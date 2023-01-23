import pytest

from ha_core.state import State
from ha_utils.ha_const import Generic
from home_alarm import HomeAlarm
from test_utils import fake_func, read_config


@pytest.fixture()
def sut():
    sut = HomeAlarm()
    return sut


@pytest.mark.asyncio
async def test_initialize(sut, monkeypatch, mocker):
    config = read_config("test_config_with_all_alerts")
    sut.args = config

    monkeypatch.setattr(sut, "get_state", fake_func(is_async=True))
    listen_state_stub = mocker.patch.object(sut, "listen_state")

    await sut.initialize()

    assert listen_state_stub.call_count == 4
    listen_state_stub.assert_any_call(sut.safe_mode_cb, "input_boolean.safe_mode")
    listen_state_stub.assert_any_call(
        sut.door_opened_cb,
        "binary_sensor.livingroom_window_contact",
        new=Generic.ON,
        old=Generic.OFF,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "safe_mode_state, ready_to_fire, fired, safe_mode_active, expected",
    [
        ("on", False, False, True, 1),
        ("on", True, False, True, 0),
        ("on", False, True, True, 0),
        ("on", False, False, False, 0),
        ("off", False, False, False, 0),
        ("off", True, False, False, 0),
        ("off", False, True, True, 0),
    ],
)
async def test_door_opened(
    sut,
    safe_mode_state,
    ready_to_fire,
    fired,
    safe_mode_active,
    expected,
    monkeypatch,
    mocker,
):
    sut.state = State()
    sut.state.ready_to_fire = ready_to_fire
    sut.state.fired = fired
    sut.safe_mode_active = safe_mode_active

    config = read_config("test_config_with_all_alerts")
    sut.safe_mode = config["safe_mode"]
    sut.activation_delay = config["activation_delay"]

    monkeypatch.setattr(sut, "friendly_name", fake_func(is_async=True))
    monkeypatch.setattr(
        sut, "get_state", fake_func(to_return=safe_mode_state, is_async=True)
    )
    monkeypatch.setattr(sut, "reset_stop_alarm", fake_func(is_async=True))

    run_in_stub = mocker.patch.object(sut, "run_in")

    sensor = "binary_sensor.livingroom_window_contact"
    await sut.door_opened_cb(sensor, "", "", "", "")

    assert run_in_stub.call_count == expected
    if expected != 0:
        run_in_stub.assert_any_call(sut.countdown, sut.activation_delay)


def test_parse_alerts(sut):
    expected_alert_ids = [
        "media_player",
        "notifier",
        "xiaomi_gateway",
        "light",
        "switch",
    ]

    sut.state = State()
    config = read_config("test_config_with_all_alerts")
    alerts = sut.parse_alerts(config["alerts"])
    alert_ids = [alert.alert_id for alert in alerts]

    assert len(alerts) == len(expected_alert_ids)
    assert alert_ids == expected_alert_ids
