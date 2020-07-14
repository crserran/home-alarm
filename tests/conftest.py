import pytest
import appdaemon.plugins.hass.hassapi as hass

from test_utils import fake_func

@pytest.fixture(autouse=True)
def hass_mock(monkeypatch):
  """
  Fixture for set up the tests, mocking appdaemon functions
  """

  monkeypatch.setattr(hass.Hass, "__init__", fake_func())
  monkeypatch.setattr(hass.Hass, "listen_state", fake_func())
  monkeypatch.setattr(hass.Hass, "log", fake_func())
  monkeypatch.setattr(hass.Hass, "run_in", fake_func(is_async=True))
  monkeypatch.setattr(hass.Hass, "call_service", fake_func(is_async=True))