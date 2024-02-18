from aiomqtt import Client
from config.mqtt import get_mqtt_client
from fastapi import Depends
from services.delivery.mqtt import MqttDelivery
from services.delivery.proto import Delivery


def get_delivery(client: Client = Depends(get_mqtt_client)) -> Delivery:
    """Get object which can send data to matrix"""

    return MqttDelivery(client)
