import pytest

from runserver import get_gae_version


def test_get_gae_version(tmpdir):
    f = tmpdir.join('version_demo.yaml')
    f.write(GAE_VERSION)
    filepath = str(f.realpath())

    assert (1, 8, 0) == get_gae_version(filepath)


def test_get_gae_version_invalid(tmpdir):
    f = tmpdir.join('version_demo.yaml')
    f.write('')
    filepath = str(f.realpath())

    with pytest.raises(ValueError):
        get_gae_version(filepath)


GAE_VERSION = u"""\
release: "1.8.0"
timestamp: 1367368689
api_versions: ['1']
supported_api_versions:
  python:
    api_versions: ['1']
  python27:
    api_versions: ['1']
  go:
    api_versions: ['go1']
"""
