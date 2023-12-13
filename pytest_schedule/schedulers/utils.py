from typing import List

from pytest_schedule.schedulers.scheduler import Scheduler
from pytest_schedule.schedulers.types import ScheduleType


def get_scheduler(schedule_type: ScheduleType) -> type[Scheduler]:
    import logging

    logger = logging.getLogger(__name__)
    logger.error(ScheduleType)
    for scheduler in get_all_schedulers():
        if scheduler.schedule_type == schedule_type:
            return scheduler
    raise TypeError(
        f"Scheduler of type {schedule_type} not found. Options are: {get_all_schedulers()}"
    )


def get_all_schedulers() -> List[type[Scheduler]]:
    return Scheduler.__subclasses__()
