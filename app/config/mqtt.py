from aiomqtt import Client

MQTT_GLOBAL_OBJ = None


def get_mqtt_client() -> Client:
    """Get mqtt client. MQTT_GLOBAL_OBJ must be initialized (in main) before calling this function."""

    return MQTT_GLOBAL_OBJ  # noqa
