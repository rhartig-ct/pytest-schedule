from typing import List

from pytest_schedule.schedulers.scheduler import Scheduler
from pytest_schedule.schedulers.types import ScheduleType
from pytest_schedule.utils import Process


class RoundRobinScheduler(Scheduler):
    schedule_type = ScheduleType.RoundRobin

    def create_schedule(self) -> List[Process]:
        """
        Uses info on tests and execution time and divides them into m buckets to be scheduled.
        RoundRobin scheduling sorts execution time longest to shortest then goes through the tests
        scheduling them to processes in a round robin fashion.

        @return List of Process Scheduler.workers long, each Process should contain the test names (pytest.Item.nodeid) the should be grouped together
        """
        schedule = [Process(i) for i in range(self.workers)]
        accending = True
        index = 0
        sorted_data = sorted(self.test_times.items(), key=lambda x: x[1], reverse=True)
        for test, time in sorted_data:
            schedule[index % self.workers].append(test, time)
            index += 1
        return schedule
