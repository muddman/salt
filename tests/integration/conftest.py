# -*- coding: utf-8 -*-
'''
    tests.integration.conftest
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Integration tests PyTest configuration/fixtures
'''
# pylint: disable=unused-argument,redefined-outer-name

# Import Python libs
from __future__ import absolute_import, unicode_literals
import logging
from collections import OrderedDict

# Import 3rd-party libs
import psutil
import pytest

log = logging.getLogger(__name__)


#@pytest.fixture(scope='package', autouse=True)
def default_session_daemons(request,
                            log_server,
                            session_salt_master,
                            session_salt_minion,
                            session_secondary_salt_minion,
                            ):

    request.session.stats_processes.update(OrderedDict((
        ('Salt Master', psutil.Process(session_salt_master.pid)),
        ('Salt Minion', psutil.Process(session_salt_minion.pid)),
        ('Salt Sub Minion', psutil.Process(session_secondary_salt_minion.pid)),
    )).items())

    # Run tests
    yield

    # Stop daemons now(they would be stopped at the end of the test run session
    for daemon in (session_secondary_salt_minion, session_salt_minion, session_salt_master):
        try:
            daemon.terminate()
        except Exception as exc:  # pylint: disable=broad-except
            log.warning('Failed to terminate daemon: %s', daemon.__class__.__name__)


# @pytest.fixture(scope='package')
# def salt_syndic_master(request, salt_factories):
#     return salt_factories.spawn_master(request, 'syndic_master', order_masters=True)


# @pytest.fixture(scope='package')
# def salt_syndic(request, salt_factories, salt_syndic_master):
#     return salt_factories.spawn_syndic(request, 'syndic', master_of_masters_id='syndic_master')


#@pytest.fixture(scope='package')
#def salt_master(request, salt_factories, salt_syndic_master):
#    return salt_factories.spawn_master(request, 'master', master_of_masters_id='syndic_master')


@pytest.fixture(scope='package')
def salt_master(request, salt_factories):
    return salt_factories.spawn_master(request, 'master')


@pytest.fixture(scope='package')
def salt_minion(request, salt_factories, salt_master):
    return salt_factories.spawn_minion(request, 'minion', master_id='master')


@pytest.fixture(scope='package')
def salt_sub_minion(request, salt_factories, salt_master):
    return salt_factories.spawn_minion(request, 'sub_minion', master_id='master')


@pytest.fixture(scope='package', autouse=True)
def bridge_pytest_and_runtests(bridge_pytest_and_runtests,
                               salt_factories,
                               # salt_syndic_master,
                               # salt_syndic,
                               salt_master,
                               salt_minion,
                               salt_sub_minion):

    yield
