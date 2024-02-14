from fastapi import WebSocket
from services.delivery.mqtt import MqttDelivery
from services.delivery.proto import Delivery


def get_delivery(websocket: WebSocket) -> Delivery:
    """Get object which can send data to matrix"""

    return MqttDelivery(websocket.app.state.amqtt_client)
