import json
from dataclasses import dataclass, field

import datetime

import pytz


def get_now():
    tz = pytz.timezone("Europe/London")
    return datetime.datetime.now(tz).isoformat()


@dataclass
class BasePayload():
    source_name: str
    raw_message: str

    def as_json(self):
        return json.dumps(self.__dict__)

@dataclass()
class TemperaturePayload(BasePayload):
    temperature: float


if __name__ == "__main__":
    print(TemperaturePayload(source_name="foo", temperature=1.2).as_json())
