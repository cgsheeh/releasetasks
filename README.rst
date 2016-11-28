===============================
Release Graphs
===============================

Mozilla Release Promotion Tasks contains code to generate release-related Taskcluster graphs.

* Free software: MPL license

Features
--------

* TODO

Testing
-------

Example test invocation using docker:
  python setup.py docker_test

Or to run a single test:
  python setup.py docker_test --test-string=test_updates.py::TestUpdates::test_requires
