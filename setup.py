#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
from distutils.spawn import find_executable
try:
    from setuptools import setup
    from setuptools import Command
except ImportError:
    from distutils.core import setup
    from distutils.cmd import Command


class DockerTestCommand(Command):
    """
    DockerTestCommand
        A custom command to run the docker test suite

        - Run all the tests
            python setup.py docker_test
        - Run all the tests in a file
            python setup.py docker_test --test-string=test_task_notification.py
        - Run all the tests in a class
            python setup.py docker_test --test-string=firefox/test_bb_update_verify.py::TestBB_UpdateVerify
        - Run a single test
            python setup.py docker_test --test-string=firefox/test_bb_update_verify.py::TestBB_UpdateVerify::test_bb_update_verify_task
        - Run test with custom docker instance
            python setup.py docker_test --docker-path="/custom/docker/path"
    """

    description = 'run the test suite with Docker'
    user_options = [
        ('test-string=', 's', 'Run test specified with test string',),
        ('docker-path=', 'd', 'Specify custom Docker binary'),
    ]

    def initialize_options(self):
        """Set defaults for options."""
        self.test_string = None
        self.docker_path = find_executable('docker')

    def finalize_options(self):
        """Post-process options"""

        # Check for docker at specified location
        if self.docker_path:
            self.docker_path = find_executable(self.docker_path)

        # Fail if docker cannot be located
        if not self.docker_path:
            assert False, "Cannot locate docker!"


    def run(self):
        """Run command"""
        command = [self.docker_path,
                   'run',
                   '--rm',
                   '-v',
                   '{pwd}:/src'.format(pwd=os.getcwd()),
                   '-ti',
                   'rail/python-test-runner',
                   '/bin/sh',
                   '-c',
                   '"cd /src &&']

        if self.test_string:
            # Append string to run specified test
            command.append('.tox/py27/bin/py.test --verbose --doctest-modules releasetasks/test/{test_string}"'
                           .format(test_string=self.test_string))
        else:
            # Append string to run all tests
            command.append('tox"')

        try:
            subprocess.check_call(' '.join(command), shell=True)
        except subprocess.CalledProcessError:
            # Catch a bad exit status, as that indicates tests failures and we do not need to print a traceback
            pass



readme = open('README.rst').read()
requirements = [
    "Jinja2",
    "taskcluster>=0.0.24",
    "arrow",
    "requests>=2.4.3,<=2.7.0",
    "PyYAML",
    "chunkify",
    "PGPy",
    "python-jose<=0.5.6",
    "redo",
]
test_requirements = [
    "pytest",
    "pytest-cov",
    "flake8",
    "mock",
    "voluptuous",
]

setup(
    name='releasetasks',
    version='0.4.0',
    description="""Mozilla Release Promotion Tasks contains code to generate
    release-related Taskcluster graphs.""",
    long_description=readme,
    author="Rail Aliiev",
    author_email='rail@mozilla.com',
    url='https://github.com/rail/releasetasks',
    packages=[
        'releasetasks',
    ],
    package_dir={'releasetasks':
                 'releasetasks'},
    include_package_data=True,
    install_requires=requirements,
    license="MPL",
    zip_safe=False,
    keywords='releasetasks',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={
        'docker_test': DockerTestCommand,
    },
)
