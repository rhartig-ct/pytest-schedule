====================
pytest-schedule
====================

Record test runtime and use this info to create a schedule to optimize runtime/core utilization.

Improve total runtime of test suites where are few long tests are slowing things down.  If you've got a test suite that could theoretically be completed on n cores in ten minutes,
but have a 10 minute test in the suite, if that test starts at the 5 minute market the whole suite will take 5 extra minutes waiting for it.


Features
--------

* Sort tests on consecutive runs by their last duration.
* Average execution time over x runs
* Fine tune scheduling with bias against larger groups of tests
* Works with `pytest-xdist`_ by pre-assigning tests to workers based on created schedule.
* Extensible scheduler system
* Round Robin, Snake, and Shortest Group schedulers


Requirements
------------

* pytest
* pytest-xdist


Installation
------------

You can install "pytest-schedule" via `pip`_::

    $ pip install git+https://github.com/rhartig-ct/pytest-schedule@initial-release


Usage
-----

Requires the use of `pytest-xdist`_ to run tests in parallel (otherwise the schedule doesn't do much good).
When used together, make sure to pass ``--dist=loadgroup`` to `pytest`_ to
ensure that tests are distributed evenly across workers.

Use --schedule to choose which scheduler is used. Current schedulers are "shortest group": assign next (sorted) test to the worker with the shortest schedule,
"round robin": assign next (sorted) test to workers in a round robin pattern, "snake": assign next (sorted) test to the worker in a snake pattern (go through all workers front to back then back to front, repeat).

RoundRobin and Snake are included more as basic examples and shouldn't be used.  RoundRobin produces a weighted schedule that where early workers are expected to take longer than later workers, Snake should always out preform it.

These schedulers will not work well with all test sets, and can even potentially slow down total execution time in certain circumstances.

Execution time recording assumes tests are run on similar hardware, on distributed setups with different hardware execution time and therefore scheduling can be off.

Shortest Group scheduler performs well on test sets with a few tests that are much longer than the rest.

Schedulers will not work on any test configuration that does not use --dist loadgroup (from xdist), since this is how it enforces its schedule.

Example command line::

    $ pytest --schedule "shortest group" -n auto --dist=loadgroup

    $ pytest --schedule "shortest group" --avg 5 -n auto --dist=loadgroup

    $ pytest --schedule "shortest group" --overhead .1 -n auto --dist=loadgroup

    $ pytest --schedule "shortest group" --no-sort-tests -n auto --dist=loadgroup


Contributing
------------
Contributions are very welcome. Tests can be run with `pytest`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-schedule" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`MIT`: http://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/klimkin/pytest-slowest-first/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`pytest-xdist`: https://github.com/pytest-dev/pytest-xdist
