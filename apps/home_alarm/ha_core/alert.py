import abc
from typing import List
import asyncio
import appdaemon.plugins.hass.hassapi as hass
from ha_core.state import State


class Alert(abc.ABC):
    def __init__(self, state: State, hass: hass.Hass, kwargs):
        self.state = state
        self.hass = hass
        self.parse_kwargs(kwargs)

    @abc.abstractmethod
    def parse_kwargs(self, kwargs) -> None:
        pass

    async def sensor_activated(self) -> None:
        pass

    async def ready_to_fire(self) -> None:
        pass

    @abc.abstractmethod
    async def alarm_fired(self) -> None:
        raise NotImplementedError

    async def alarm_stopped(self) -> None:
        pass


class AlertList:
    def __init__(self, alerts: List[Alert]) -> None:
        self.alerts = alerts

    def sensor_activated(self) -> None:
        for alert in self.alerts:
            asyncio.create_task(alert.sensor_activated())

    def ready_to_fire(self) -> None:
        for alert in self.alerts:
            asyncio.create_task(alert.ready_to_fire())

    def alarm_fired(self, sensor_fired) -> None:
        for alert in self.alerts:
            asyncio.create_task(alert.alarm_fired(sensor_fired))

    def alarm_stopped(self) -> None:
        for alert in self.alerts:
            asyncio.create_task(alert.alarm_stopped())
