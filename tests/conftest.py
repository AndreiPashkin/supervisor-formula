"""Fixtures and hooks for the tests."""
from functools import wraps
import json
import os
import subprocess

import pytest
import yaml

from tests.utils import normalize_ini


def pytest_addoption(parser):
    """Custom options."""
    parser.addoption("--lxc-snapshot", action="store",
                     help="Name of a container snapshot, that should be used "
                          "by 'lxd_snapshot' fixture.")


@pytest.fixture(scope='function')
def lxc_snapshot(request, TestinfraBackend):
    """Provides a Vagrant VM in a pristine state, by reverting it to
    a snapshot, defined by `--vagrant-snapshot` option.
    Also requires `--vagrantfile` option, with location of Vagrantfile
    as a value.
    """
    snapshot = request.config.getoption('--lxc-snapshot')
    if snapshot is None:
        pytest.exit("'lxc_snapshot' fixture require '--lxc-snapshot' option.")
    stop = ['lxc-stop',
            '--name', TestinfraBackend.hostname]
    restore = ['lxc-snapshot',
               '--name', TestinfraBackend.hostname,
               '--restore', snapshot]
    start = ['lxc-start',
            '--name', TestinfraBackend.hostname]
    if TestinfraBackend.sudo:
        stop, restore, start = [['sudo'] + cmd
                                      for cmd in [stop, restore, start]]
    subprocess.call(stop)
    subprocess.check_call(restore)
    subprocess.check_call(start)


@pytest.fixture
def grains(Command):
    """Grains."""
    cmd = Command('salt-call --out=json grains.items')
    return json.loads(cmd.stdout)['local']


@pytest.fixture
def pillar(Command):
    """Pillar data."""
    cmd = Command('salt-call --out=json pillar.items')
    return json.loads(cmd.stdout)['local']


DEFAULTS = {
    'Debian': {
        'conf_file': '/etc/supervisord.conf',
        'init_script_file': '/etc/init.d/supervisor'
    }
}


DEFAULT_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              os.path.pardir,
                              'supervisor', 'service', 'default_config.yml')


@pytest.fixture
def supervisor_config(File, grains, pillar):
    """Supervisor configuration file."""
    try:
        path = reduce(
            lambda x, y: x[y],
            'supervisor.lookup.service.installed.conf_file',
            pillar
        )
    except KeyError:
        path = DEFAULTS[grains['os_family']]['conf_file']

    return File(path)


@pytest.fixture
def default_config():
    """Default Supervisor configuration."""
    return yaml.load(open(DEFAULT_CONFIG).read())


@pytest.fixture
def is_config_exists(supervisor_config):
    """Function, that checks, if supervisor config is exists and owned by
    'root'.
    """
    return wraps(is_config_exists)(
        lambda: (supervisor_config.is_file and
                 supervisor_config.exists and
                 (supervisor_config.user == 'root'))
    )


@pytest.fixture
def is_config_the_default(supervisor_config):
    """Function, that checks, if Supervisor config equals to default one."""
    return wraps(is_config_the_default)(
        lambda: (normalize_ini(yaml.load(open(DEFAULT_CONFIG).read())) ==
                 normalize_ini(supervisor_config.content))
    )


@pytest.fixture
def is_supervisor_enabled(Service):
    """Function, that checks if Supervisor service is enabled."""
    return wraps(is_supervisor_enabled)(
        lambda: Service('supervisor').is_enabled
    )


@pytest.fixture
def is_supervisor_running(Service):
    """Function, that checks if Supervisor service is running."""
    return wraps(is_supervisor_running)(
        lambda: Service('supervisor').is_running
    )
