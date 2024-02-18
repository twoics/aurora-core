from services.preprocess.hex_stream import RGBPreprocess
from services.preprocess.proto import Preprocess


def get_preprocess() -> Preprocess:
    """Get stream preprocess which handle incoming ws messages"""

    return RGBPreprocess()
