from __future__ import annotations

import os
import re
from statistics import mean

import pytest

from pytest_schedule.schedulers.types import ScheduleType
from pytest_schedule.schedulers.utils import get_scheduler
from pytest_schedule.utils import assign_xdist_workers

_execution_time_key = pytest.StashKey[float]()


@pytest.hookimpl
def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup(
        "pytest_schedule",
        "Options to modify how tests are scheduled across workers. Requires -n > 1 and --dist loadgroup",
    )
    group.addoption(
        "--schedule",
        dest="schedule",
        action="store",
        default="default",
        type=str,
        choices=[e.value for e in ScheduleType],
        help="Select scheduling type",
    )
    group.addoption(
        "--avg",
        "--average",
        dest="exec_average",
        action="store",
        default=3,
        type=int,
        help="Average test execution time over this many runs.",
    )
    group.addoption(
        "--cache-schedule",
        dest="cache_schedule",
        action="store_true",
        default=False,
        help="Write planned schedule to cache. This does not reuse the schedule and is intended for debugging/optimization.",
    )
    group.addoption(
        "--oh",
        "--overhead",
        dest="test_overhead",
        action="store",
        default=0,
        type=float,
        help="Overhead penelty for tests. Increasing this value penalizes test groups with more tests.",
    )
    group.addoption(
        "--no-sort-tests",
        dest="sort_tests",
        action="store_false",
        default=True,
        help="Prevent the sorting of tests. Some schedulers may ignore this option. For those that don't the tests will not be run in longest to shortest order. This helps the completion percentage track the real completion time.",
    )


# Must go before xdist hook so the markers are in place
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    execution_times = {}
    config.option.dist = "loadgroup"
    for item in items:
        cache_key = "execution_times/{}".format(
            re.sub(r"[^\w_. -]", "_", item.nodeid.split("@")[0])
        )
        test_times = config.cache.get(cache_key, [0])
        avg_time = mean(test_times[-config.option.exec_average :])
        execution_times[item.nodeid] = avg_time + config.option.test_overhead

    if config.option.sort_tests:
        items.sort(key=lambda item: execution_times.get(item.nodeid, 0), reverse=True)

    config.option.schedule = ScheduleType(config.option.schedule)
    if config.option.schedule != ScheduleType.Default:
        xdist_workers = int(os.environ.get("PYTEST_XDIST_WORKER_COUNT", 0))
        if xdist_workers > 1:
            scheduler_type = config.option.schedule
            scheduler = get_scheduler(scheduler_type)(
                execution_times, items, xdist_workers
            )
            schedule = scheduler.create_schedule()
            if config.option.cache_schedule:
                for data in schedule:
                    config.cache.set(f"schedule/{data.id}", data.to_dict())
            if config.option.dist == "loadgroup":
                assign_xdist_workers(items, schedule)

    for item in items:
        item.stash[_execution_time_key] = 0


@pytest.hookimpl
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    """Save aggregated duration of the item calls to the cache."""

    # Aggregate setup and call phases
    item.stash[_execution_time_key] += call.duration

    # Only write to cache at the end, not for each step (collect, setup, call, teardown)
    if call.when != "teardown":
        return

    # regex makes the generated path safe for windows
    # xdist adds '@{marker_name}' to track files with --dist loadgroup which will be a different name from what is read in the modifyitems hook
    cache_key = "execution_times/{}".format(
        re.sub(r"[^\w_. -]", "_", item.nodeid.split("@")[0])
    )
    execution_times = item.config.cache.get(cache_key, [])
    execution_times.append(item.stash[_execution_time_key])
    item.config.cache.set(cache_key, execution_times)
