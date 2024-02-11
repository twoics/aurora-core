from typing import List
from typing import Tuple

from app.models import User
from app.services.handler.proto import StreamHandler


class HexHandler(StreamHandler):
    @staticmethod
    def to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Converts a hex color to an RGB tuple"""

        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))  # noqa

    async def handle(self, data, uuid: str, user: User) -> List[int] | None:
        """Handle incoming messages and convert them to send on matrix"""

        try:
            return [i_rgb for hex_val in data for i_rgb in self.to_rgb(hex_val)]
        except (ValueError, TypeError):
            return None
