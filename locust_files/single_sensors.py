import datetime
import random
import time

import locust

DEVICE_ID_1 = "00000000-0000-0000-1000-000000000000"


class SensorUser(locust.HttpUser):
    """
    Locust class for sensors posting a single measurements to the API.
    """

    @locust.task
    def post_measurement(self):
        sent_at = datetime.datetime.now().isoformat()

        self.client.post(
            "/measurements",
            json={
                "device_id": DEVICE_ID_1,
                "value": random.randint(0, 100),
                "measurement_type": "voltage",
                "measured_at": sent_at,
                "sent_at": sent_at,
            },
        )
        time.sleep(0.25)
