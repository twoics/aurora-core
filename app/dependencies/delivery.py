from fastapi import WebSocket

from app.services.delivery.mqtt import MqttDelivery
from app.services.delivery.proto import Delivery


def get_delivery(websocket: WebSocket) -> Delivery:
    """Get object which can send data to matrix"""

    return MqttDelivery(websocket.app.state.amqtt_client)
