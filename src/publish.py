import json

import requests as requests
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

from config import CONFIG
from payload import TemperaturePayload


def get_queue():
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    credentials_provider = auth.AwsCredentialsProvider.new_default_chain(
        client_bootstrap
    )

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=CONFIG["AWS"]["endpoint"],
        credentials_provider=credentials_provider,
        port=443,
        cert_filepath=CONFIG["AWS"]["certs"]["certificate"],
        pri_key_filepath=CONFIG["AWS"]["certs"]["private"],
        client_bootstrap=client_bootstrap,
        client_id=CONFIG["AWS"]["client_id"],
        clean_session=False,
        keep_alive_secs=60,
    )

    connect_future = mqtt_connection.connect()
    connect_future.result()
    return mqtt_connection


def publish_openweather_message(queue):
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": CONFIG["openweather"]["lat"],
        "lon": CONFIG["openweather"]["long"],
        "appid": CONFIG["openweather"]["api_key"],
        "units": "metric",
    }
    req = requests.get(url, params=params)
    json_data = req.json()
    payload = TemperaturePayload(
        source_name="openweather",
        raw_message=json_data,
        temperature=json_data["main"]["temp"],
    )
    queue.publish(
        topic="source/openweather",
        payload=payload.as_json(),
        qos=mqtt.QoS.AT_LEAST_ONCE,
    )


if __name__ == "__main__":

    queue = get_queue()
    publish_openweather_message(queue)
