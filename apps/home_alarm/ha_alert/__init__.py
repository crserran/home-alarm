from ha_utils import utils
from ha_core.alert import Alert

def get_alerts() -> dict:
  alerts = utils.get_subclasses(__file__, __package__, Alert)
  return {
    alert.alert_id: alert for alert in alerts
  } 