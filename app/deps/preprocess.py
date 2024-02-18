from services.preprocess.proto import Preprocess
from services.preprocess.rgb import RGBPreprocess


def get_preprocess() -> Preprocess:
    """Get stream preprocess which handle incoming ws messages"""

    return RGBPreprocess()
