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
    parser.addoption("--vagrant-snapshot", action="store",
                     help="Name of the VM snapshot, that should be used by "
                          "'vagrant' fixture.")
    parser.addoption("--vagrantfile", action="store",
                     help="'Vagrantfile' for 'vagrant' fixture.")


@pytest.fixture
def vagrant(request):
    """Provides a Vagrant VM in a pristine state, by reverting it to
    a snapshot, defined by `--vagrant-snapshot` option.
    Also requires `--vagrantfile` option, with location of Vagrantfile
    as a value.
    """
    vagrantfile = request.config.getoption('--vagrantfile')
    snapshot = request.config.getoption('--vagrant-snapshot')
    if snapshot is None:
        pytest.exit("'vagrant' fixture require '--vagrant-snapshot' option.")
    if vagrantfile is None:
        pytest.exit("'vagrant' fixture require '--vagrantfile' option.")
    vagrantfile_dir = os.path.dirname(vagrantfile)
    subprocess.check_call(
        ['vagrant', 'snapshot', 'restore', snapshot],
        cwd=vagrantfile_dir
    )


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
