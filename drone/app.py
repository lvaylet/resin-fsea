#!/usr/bin/env python3
# coding: utf-8

"""
This module is responsible for simulating a drone.

The drone is associated with a unique identifier. It publishes its geo-location
coordinates to a central MQTT broker in real-time through a cellular modem
connection. Cellular modem connections are expensive, so there is a big emphasis
on using as little data as possible.
"""

import json
import logging
import os
import random
import time

import paho.mqtt.client as mqtt

# region Constants
MQTT_HOST = os.environ['MQTT_HOST']
MQTT_PORT = int(os.environ['MQTT_PORT'])
MQTT_TOPIC = 'drone/position'  # MQTT topic to publish to


# endregion


# region Logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


# endregion


# region Class Definitions
class Drone:
    """
    Properties like UUID, name, latitude and longitude are private and can only
    be set in the constructor. They are exposed through getters only (using the
    @property decorator). The move() method is responsible for movng the drone
    to a different location and update the latitude and longitude.
    """

    def __init__(self, uuid, name, initial_latitude, initial_longitude):
        """
        :param uuid: Unique identifier
        :param name: Display name
        :param initial_latitude: Initial latitude, in decimal degrees
        :param initial_longitude: Initial longitude, in decimal degrees
        :type uuid: str
        :type name: str
        :type initial_latitude: float
        :type initial_longitude: float
        """
        self.__uuid = uuid
        self.__name = name
        self.__latitude = initial_latitude
        self.__longitude = initial_longitude

    @property
    def uuid(self):
        return self.__uuid

    @property
    def name(self):
        return self.__name

    @property
    def latitude(self):
        return self.__latitude

    @property
    def longitude(self):
        return self.__longitude

    def move(self):
        self.__latitude += random.uniform(-0.001, 0.001)
        self.__longitude += random.uniform(-0.001, 0.001)


# endregion


# region Callbacks
def on_connect(client, userdata, flags, result_code):
    """
    The callback for when the MQTT client receives a CONNACK response from the server.
    """
    if result_code == 0:
        logging.info('Successfully connected to MQTT broker.')
    else:
        logging.info('Failed to connect to MQTT broker with result code {result_code}.')


# endregion


if __name__ == '__main__':

    logging.info('Instantiating MQTT client...')
    client = mqtt.Client()
    logging.info('Defining `on_connect` callback of MQTT client...')
    client.on_connect = on_connect  # called when the broker responds to the connection request

    logging.info('Establishing connection to central MQTT broker...')
    client.connect(host=MQTT_HOST, port=MQTT_PORT)

    logging.info('Starting background thread to handle the network connection and sending/receiving data...')
    client.loop_start()

    logging.info('Instantiating drone at initial position (48.8581824, 2.212730400000055)...')
    drone = Drone(
        uuid=os.environ['UUID'],  # raises `KeyError` if not defined
        name=os.environ['NAME'],  # raises `KeyError` if not defined
        initial_latitude=48.8581824,  # TODO Use env (like for UUID and NAME)
        initial_longitude=2.212730400000055  # TODO Use env (like for UUID and NAME)
    )

    # Publish geo-location and metadata every 5 seconds
    while True:
        timestamp = int(time.time()),  # number of seconds since the epoch (January 1st, 1970 in UTC)
        # TODO JSON is not the best option to minimize data usage over cellular connection. Investigate binary frames.
        payload = {
            'ts': timestamp,
            'uuid': drone.uuid,
            'name': drone.name,
            'latitude': drone.latitude,
            'longitude': drone.longitude
        }

        logging.info('Publishing current position to topic [%s]...', MQTT_TOPIC)
        client.publish(MQTT_TOPIC, json.dumps(payload))

        time.sleep(5)

        drone.move()
