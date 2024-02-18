from services.preprocess.hex_stream import Preprocess
from services.preprocess.proto import PreprocessProto


def get_stream_handler() -> PreprocessProto:
    """Get stream preprocess which handle incoming ws messages"""

    return Preprocess()
