"""Utilities and helpers for the tests."""
from ConfigParser import ConfigParser
from cStringIO import StringIO
import json
import os


def summary(results):
    """Extracts summary from output of Salt, formatted as JSON."""
    if not hasattr(results, 'keys'):
        results = json.loads(results)

    succeed = 0
    failed = 0
    changed = 0
    for _, state in results.iteritems():
        for _, results in state.iteritems():
            if results['result']:
                succeed += 1
            else:
                failed += 1
            changed += len(results['changes'])
    return {'succeed': succeed, 'failed': failed, 'changed': changed}


def normalize_ini(data):
    """Brings INI config to a normalized form, suitable for comparing.

    Accepts dicts, JSON strings, paths to INI configs and ConfigParser
    instances.
    """
    if hasattr(data, 'lower'):
        if os.path.exists(data):
            data = open(data).read()
        parser = ConfigParser()
        parser.readfp(StringIO(data))
    elif hasattr(data, 'iteritems'):
        parser = ConfigParser()
        for section, items in data.iteritems():
            section = str(section)
            parser.add_section(section)
            if items is None:
                continue
            for option, value in dict(items).iteritems():
                parser.set(section, str(option), str(value))
    elif hasattr(data, 'sections'):
        parser = data
    else:
        raise TypeError
    normalized = {}
    for section in parser.sections():
        for option, value in parser.items(section):
            normalized.setdefault(section, {})[option] = value
    return normalized
