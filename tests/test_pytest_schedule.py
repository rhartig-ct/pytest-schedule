import logging

import pytest

from pytest_schedule.schedulers.round_robin import RoundRobinScheduler
from pytest_schedule.schedulers.shortest_group import ShortestGroupScheduler
from pytest_schedule.schedulers.snake import SnakeScheduler

logger = logging.getLogger(__name__)


def test_help_message(testdir: pytest.Pytester):
    result = testdir.runpytest(
        "--help",
    )
    result.stdout.fnmatch_lines(
        [
            "*--schedule={round robin,snake,shortest group,default}",
            "*--avg=EXEC_AVERAGE, --average=EXEC_AVERAGE",
            "*--cache-schedule*",
            "*--oh=TEST_OVERHEAD, --overhead=TEST_OVERHEAD",
        ]
    )


def test_reorders_tests(testdir: pytest.Pytester):
    testdir.makepyfile(
        """
        import time
        def test_1():
            time.sleep(0.1)
        def test_2():
            time.sleep(0.2)
        def test_3():
            time.sleep(0.3)
        def test_4():
            time.sleep(0.4)
        def test_5():
            time.sleep(0.5)
        def test_6():
            time.sleep(0.6)
        """
    )
    result = testdir.runpytest()
    result = testdir.runpytest("--collect-only")
    result.stdout.fnmatch_lines(
        [
            "*test_6*",
            "*test_5*",
            "*test_4*",
            "*test_3*",
            "*test_2*",
            "*test_1*",
        ]
    )


def test_snake_scheduler():
    test_times = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "11": 11,
        "12": 12,
        "13": 13,
        "14": 14,
        "15": 15,
        "16": 16,
        "17": 17,
    }

    scheduler = SnakeScheduler(test_times, [], 4)
    schedule = scheduler.create_schedule()

    assert schedule[0].jobs == ["17", "10", "9", "2", "1"]
    assert schedule[1].jobs == ["16", "11", "8", "3", "0"]
    assert schedule[2].jobs == ["15", "12", "7", "4"]
    assert schedule[3].jobs == ["14", "13", "6", "5"]


def test_shortest_group_scheduler():
    test_times = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "11": 11,
        "12": 12,
        "13": 13,
        "14": 14,
        "15": 15,
        "16": 16,
        "17": 17,
    }

    scheduler = ShortestGroupScheduler(test_times, [], 4)
    schedule = scheduler.create_schedule()

    # With clean data like this shortest group is the same as snake, but doesn't schedule the 0 since no time data is available for it
    assert schedule[0].jobs == ["17", "10", "9", "2", "1"]
    assert schedule[1].jobs == ["16", "11", "8", "3"]
    assert schedule[2].jobs == ["15", "12", "7", "4"]
    assert schedule[3].jobs == ["14", "13", "6", "5"]

    test_times = {
        "0": 95.1,
        "1": 66.6,
        "2": 7.8,
        "3": 101.9,
        "4": 52.6,
        "5": 10.5,
        "6": 106.1,
        "7": 2.6,
        "8": 21.4,
        "9": 26.2,
        "10": 0.6,
        "11": 111.8,
        "12": 69.2,
        "13": 57.9,
        "14": 51.1,
        "15": 78.0,
        "16": 87.8,
        "17": 21.6,
    }

    scheduler = ShortestGroupScheduler(test_times, [], 4)
    schedule = scheduler.create_schedule()

    assert schedule[0].jobs == ["11", "1", "4", "5"]
    assert schedule[1].jobs == ["6", "12", "13", "7", "10"]
    assert schedule[2].jobs == ["3", "15", "14", "2"]
    assert schedule[3].jobs == ["0", "16", "9", "17", "8"]


def test_round_robin_scheduler():
    test_times = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "11": 11,
        "12": 12,
        "13": 13,
        "14": 14,
        "15": 15,
        "16": 16,
        "17": 17,
    }

    scheduler = RoundRobinScheduler(test_times, [], 4)
    schedule = scheduler.create_schedule()

    assert schedule[0].jobs == ["17", "13", "9", "5", "1"]
    assert schedule[1].jobs == ["16", "12", "8", "4", "0"]
    assert schedule[2].jobs == ["15", "11", "7", "3"]
    assert schedule[3].jobs == ["14", "10", "6", "2"]
