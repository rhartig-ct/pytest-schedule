from typing import List

from pytest_schedule.schedulers.scheduler import Scheduler
from pytest_schedule.schedulers.types import ScheduleType
from pytest_schedule.utils import Process


class ShortestGroupScheduler(Scheduler):
    schedule_type = ScheduleType.ShortestGroup

    def create_schedule(self) -> List[Process]:
        """
        Uses info on tests and execution time and divides them into m buckets to be scheduled.
        ShortestGroup scheduling sorts execution time longest to shortest then goes through the tests
        scheduling them on the process with the current shortest workload.

        @return List of Process Scheduler.workers long, each Process should contain the test names (pytest.Item.nodeid) the should be grouped together
        """
        max_value = sum(self.test_times.values()) + 1
        schedule = [Process(i) for i in range(self.workers)]
        sorted_data = sorted(self.test_times.items(), key=lambda x: x[1], reverse=True)
        for test, time in sorted_data:
            if time == 0:
                continue
            min = max_value
            target_process = Process()
            for process in schedule:
                if process.job_time_sum < min:
                    min = process.job_time_sum
                    target_process = process
            target_process.append(test, time)

        return schedule
