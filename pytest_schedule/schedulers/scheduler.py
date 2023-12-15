from typing import Dict, List

from pytest import Item

from pytest_schedule.schedulers.types import ScheduleType
from pytest_schedule.utils import Process


class Scheduler:
    schedule_type = ScheduleType.Default

    def __init__(self, test_times: Dict, items: List[Item], workers: int, **kwargs):
        self.test_times = test_times
        self.items = items
        self.workers = workers

    def create_schedule(self) -> List[Process]:
        """
        Uses info on tests and execution time and divides them into m buckets to be scheduled

        @return List of Process m long, each Process should contain the test names (pytest.Item.nodeid) the should be grouped together
        """
        raise NotImplementedError(
            "Scheduler base class is not implemented, use a subclass."
        )
