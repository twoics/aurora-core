from services.handler.hex_stream import HexHandler
from services.handler.proto import StreamHandler


def get_stream_handler() -> StreamHandler:
    """Get stream handler which handle incoming ws messages"""

    return HexHandler()
