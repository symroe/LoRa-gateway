import requests as requests
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

from config import CONFIG

event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
credentials_provider = auth.AwsCredentialsProvider.new_default_chain(client_bootstrap)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=CONFIG["AWS"]["endpoint"],
    # region="eu-west-2",
    credentials_provider=credentials_provider,
    port=443,
    cert_filepath=CONFIG["AWS"]["certs"]["certificate"],
    pri_key_filepath=CONFIG["AWS"]["certs"]["private"],
    client_bootstrap=client_bootstrap,
    # ca_filepath=CONFIG["AWS"]["endpoint"],
    # on_connection_interrupted=on_connection_interrupted,
    # on_connection_resumed=on_connection_resumed,
    client_id=CONFIG["AWS"]["client_id"],
    clean_session=False,
    keep_alive_secs=60,
)

# connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
# connect_future.result()
# print("Connected!")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")
print("publishing")


def get_openweather_message():
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": CONFIG["openweather"]["lat"],
        "lon": CONFIG["openweather"]["long"],
        "appid": CONFIG["openweather"]["api_key"],
    }
    print(params)
    req = requests.get(url, params=params)
    print(req.url)
    json = req.json()
    print(json)
    return json


mqtt_connection.publish(topic="openweather", payload=get_openweather_message(), qos=mqtt.QoS.AT_LEAST_ONCE)
