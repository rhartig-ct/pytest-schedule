from typing import Dict, List

from pytest_schedule.schedulers.scheduler import Scheduler
from pytest_schedule.schedulers.types import ScheduleType
from pytest_schedule.utils import Process


class SnakeScheduler(Scheduler):
    schedule_type = ScheduleType.Snake

    def create_schedule(self) -> List[Process]:
        """
        Uses info on tests and execution time and divides them into m buckets to be scheduled.
        Snake scheduling sorts execution time longest to shortest loops over the processes front to back then back to front:
            Tests are scheduled on nodes in this order with -n=4: 0, 1, 2, 3, 3, 2, 1, 0

        @return List of Process Scheduler.workers long, each Process should contain the test names (pytest.Item.nodeid) the should be grouped together
        """
        schedule = [Process(i) for i in range(self.workers)]
        accending = True
        index = 0
        sorted_data = sorted(self.test_times.items(), key=lambda x: x[1], reverse=True)
        for test, time in sorted_data:
            schedule[index].append(test, time)
            if accending:
                if index == self.workers - 1:
                    # Don't increase index so the last element triggers twice "snaking" back to the front
                    accending = False
                else:
                    index += 1
            else:
                if index == 0:
                    # Don't decrease index so the first element triggers twice "snaking" back to the end
                    accending = True
                else:
                    index -= 1
        return schedule
