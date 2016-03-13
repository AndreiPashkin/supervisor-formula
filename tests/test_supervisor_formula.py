"""Tests for supervisor-formula."""
import json
import pipes

import pytest

from tests.utils import summary


@pytest.mark.usefixtures('lxd_snapshot')
def test_service_configured(
    Command, is_config_exists, is_config_the_default,
    is_supervisor_enabled, is_supervisor_running
):
    """'supervisor.service.configured' state generates a config."""
    configured = Command('salt-call --out=json '
                         'state.sls supervisor.service.configured')
    assert summary(configured.stdout)['failed'] == 0, configured.stdout

    assert is_config_exists()
    assert is_config_the_default()

    assert not is_supervisor_enabled()
    assert not is_supervisor_running()


@pytest.mark.usefixtures('lxd_snapshot')
def test_service_configured_idempotent(Command):
    """'supervisor.service.configured' state is idempotent."""
    for _ in range(2):
        configured = Command('salt-call --out=json '
                             'state.sls supervisor.service.configured')
        actual_summary = summary(configured.stdout)
        assert actual_summary['failed'] == 0, configured.stdout

    assert actual_summary['changed'] == 0, configured.stdout


@pytest.mark.usefixtures('lxd_snapshot')
def test_service_installed(
    Command, is_config_exists, is_config_the_default,
    is_supervisor_enabled, is_supervisor_running
):
    """'supervisor.service.installed' state generates config and
    installs Supervisor.
    """
    installed = Command('salt-call --out=json '
                        'state.sls supervisor.service.installed')
    assert summary(installed.stdout)['failed'] == 0, installed.stdout

    assert is_config_exists()
    assert is_config_the_default()

    assert not is_supervisor_enabled()
    assert not is_supervisor_running()


@pytest.mark.usefixtures('lxd_snapshot')
def test_service_installed_idempotent(Command):
    """'supervisor.service.installed' state is idempotent."""
    for _ in range(2):
        installed = Command('salt-call --out=json '
                      'state.sls supervisor.service.installed')
        actual_summary = summary(installed.stdout)
        assert actual_summary['failed'] == 0, installed.stdout

    assert actual_summary['changed'] == 0, installed.stdout


@pytest.mark.usefixtures('lxd_snapshot')
def test_service_running(
    Command, is_config_exists, is_config_the_default,
    is_supervisor_enabled, is_supervisor_running
):
    """'supervisor.service.running' state generates config,
    installs Supervisor and creates, enables and launches a service.
    """
    running = Command('salt-call --out=json '
                      'state.sls supervisor.service.running')
    assert summary(running.stdout)['failed'] == 0, running.stdout

    assert is_supervisor_enabled()
    assert is_supervisor_running()

    assert is_config_exists()

    assert is_config_the_default()


@pytest.mark.usefixtures('lxd_snapshot')
def test_service_running_idempotent(Command):
    """'supervisor.service.running' is idempotent."""
    for _ in range(2):
        running = Command('salt-call --out=json '
                          'state.sls supervisor.service.running')
        actual_summary = summary(running.stdout)
        assert actual_summary['failed'] == 0, running.stdout

    assert actual_summary['changed'] == 0, running.stdout


@pytest.mark.usefixtures('lxd_snapshot')
def test_service_dead(Command, is_supervisor_enabled, is_supervisor_running):
    """'supervisor.service.dead' state disables and shuts down
    the service.
    """
    running = Command('salt-call --out=json '
                      'state.sls supervisor.service.running')
    assert summary(running.stdout)['failed'] == 0, running.stdout
    dead = Command('salt-call --out=json '
                   'state.sls supervisor.service.dead')
    assert summary(dead.stdout)['failed'] == 0, dead.stdout

    assert not is_supervisor_enabled()
    assert not is_supervisor_running()


@pytest.mark.usefixtures('lxd_snapshot')
def test_service_dead_idempotent(Command):
    """'supervisor.service.dead' state is idempotent."""
    running = Command('salt-call --out=json '
                      'state.sls supervisor.service.running')
    assert summary(running.stdout)['failed'] == 0, running.stdout
    for _ in range(2):
        dead = Command('salt-call --out=json '
                       'state.sls supervisor.service.dead')
        actual_summary = summary(dead.stdout)
        assert actual_summary['failed'] == 0, dead.stdout

    assert actual_summary['changed'] == 0, dead.stdout


@pytest.fixture
def dummy():
    """Pillar, that defines a simple supervisor process."""
    return {'supervisor': {'lookup': {'processes': {'running': {
        'dummy': {
            'settings': {
                'command': 'sh -c "while true; do sleep 10; done"'
            }
        }
    }}}}}


@pytest.mark.usefixtures('lxd_snapshot')
def test_processes_running(Command, is_supervisor_enabled,
                           is_supervisor_running, dummy):
    """'supervisor.processes.running' state generates config,
    installs Supervisor, creates, enables and launches a service and
    runs a Supervisor process, according to a configuration, provided by
    user of the formula.
    """
    running = Command('salt-call --out=json '
                      'state.sls supervisor.processes.running pillar=%s' %
                      pipes.quote(json.dumps(dummy)))
    assert summary(running.stdout)['failed'] == 0, running.stdout

    assert is_supervisor_enabled()
    assert is_supervisor_running()

    status = Command('supervisorctl status')
    assert 'RUNNING' in status.stdout


@pytest.mark.usefixtures('lxd_snapshot')
def test_processes_running_idempotent(Command, dummy):
    """'supervisor.processes.running' state is idempotent."""
    for _ in range(2):
        running = Command(
            'salt-call --out=json '
            'state.sls supervisor.processes.running pillar=%s' %
            pipes.quote(json.dumps(dummy))
        )
        actual_summary = summary(running.stdout)
        assert actual_summary['failed'] == 0, running.stdout

    assert actual_summary['changed'] == 0, running.stdout
