from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
from dotenv import load_dotenv
import os
import sys
import threading
import time
import json


class MQTT:

    def __init__(self):
        self.received_count = 0
        self.set_count = 10
        self.received_all_event = threading.Event()

        self.endpoint = None
        self.port = None
        self.cert_filepath = None
        self.pri_key_filepath = None
        self.ca_filepath = None
        self.client_id = None

        self.message_topic = []

        self.mqtt_connection = None
        self.connect_future = None

        self.subscribe_future = []
        self.packet_id = []
        self.subscribe_result = []

        self.disconnect_future = None

    # Callback when connection is accidentally lost.
    def on_connection_interrupted(self, connection, error, **kwargs):
        print("Connection interrupted. error: {}".format(error))

    def on_resubscribe_complete(self, resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        print("Resubscribe results: {}".format(resubscribe_results))

        for topic, qos in resubscribe_results['topics']:
            if qos is None:
                sys.exit("Server rejected resubscribe to topic: {}".format(topic))

    # Callback when an interrupted connection is re-established.
    def on_connection_resumed(self, connection, return_code, session_present, **kwargs):
        print("Connection resumed. return code: {} session present: {}".format(return_code, session_present))

        if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
            print("Session did not persist. Resubscribing to existing topics...")
            resubscribe_future, _ = connection.resubscribe_existing_topics()

            # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
            # evaluate result with a callback instead.
            resubscribe_future.add_done_callback(self.on_resubscribe_complete)


    # Callback when the subscribed topic receives a message
    def on_message_received(self, topic, payload, dup, qos, retain, **kwargs):
        print("Received message from topic '{}': {}".format(topic, payload))
        
        self.received_count += 1
        if self.received_count == self.set_count:
            self.received_all_event.set()

    # Callback when the connection successfully connects
    def on_connection_success(self, connection, callback_data):
        assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
        print("Connection Successful with return code: {} session present: {}".format(callback_data.return_code, callback_data.session_present))

    # Callback when a connection attempt fails
    def on_connection_failure(self, connection, callback_data):
        assert isinstance(callback_data, mqtt.OnConnectionFailureData)
        print("Connection failed with error code: {}".format(callback_data.error))

    # Callback when a connection has been disconnected or shutdown successfully
    def on_connection_closed(self, connection, callback_data):
        print("Connection closed")


class MQTTBuilder(MQTT):

    def __init__(self):
        MQTT.__init__(self)
    
    # setting parameters
    def set_endpoint(self, endpoint):
        self.endpoint = endpoint
        return self
    
    def set_port(self, port=8883):
        self.port = port
        return self

    def set_cert_filepath(self, cert_filepath):
        self.cert_filepath = cert_filepath
        return self

    def set_pri_key_filepath(self, pri_key_filepath):
        self.pri_key_filepath = pri_key_filepath
        return self

    def set_ca_filepath(self, ca_filepath):
        self.ca_filepath = ca_filepath
        return self

    def set_client_id(self, client_id='A104'):
        self.client_id = client_id
        return self
    
    # Create a MQTT connection from parameters
    def set_connection(self):
        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.endpoint,
            port=self.port,
            cert_filepath=self.cert_filepath,
            pri_key_filepath=self.pri_key_filepath,
            ca_filepath=self.ca_filepath,
            on_connection_interrupted=self.on_connection_interrupted,
            on_connection_resumed=self.on_connection_resumed,
            client_id=self.client_id,
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=None,
            on_connection_success=self.on_connection_success,
            on_connection_failure=self.on_connection_failure,
            on_connection_closed=self.on_connection_closed)

        self.connect_future = self.mqtt_connection.connect()

        # Future.result() waits until a result is available
        self.connect_future.result()
        print("Connected!")

        return self

    # add topics for subscribing
    def add_topic(self, message_topic):
        self.message_topic.append(message_topic)

        print("Subscribing to topic '{}'...".format(message_topic))
        subscribe_future, packet_id = self.mqtt_connection.subscribe(
            topic=message_topic,
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=self.message_callback or self.on_message_received)

        self.subscribe_future.append(subscribe_future)
        self.packet_id.append(packet_id)

        subscribe_result = subscribe_future.result()
        self.subscribe_result.append(subscribe_result)
        print("Subscribed with {}".format(str(subscribe_result['qos'])))

        return self

    # Publish MQTT message
    def publish_message(self, topic, message_string):
        message = "{}".format(message_string)
        print("Publishing message to topic '{}': {}".format(topic, message_string))
        message_json = json.dumps(message)
        self.mqtt_connection.publish(
            topic=topic,
            payload=message_json,
            qos=mqtt.QoS.AT_LEAST_ONCE)

    # Disconnecting from AWS IoT
    def set_disconnection(self):
        print("Disconnecting...")
        self.disconnect_future = self.mqtt_connection.disconnect()
        self.disconnect_future.result()
        print("Disconnected!")

        return self
    
    def set_message_callback(self, callback):
        self.message_callback = callback
        return self

