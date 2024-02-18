from typing import List
from typing import Tuple

from models import Matrix
from models import User
from services.preprocess.proto import Preprocess


class RGBPreprocess(Preprocess):
    @staticmethod
    def to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Converts a hex color to an RGB tuple"""

        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))  # noqa

    async def handle(self, data, matrix: Matrix, user: User) -> List[int] | None:
        """Handle incoming messages and convert them to send on matrix"""

        try:
            if len(data) > matrix.resolution:
                return None

            return [i_rgb for hex_val in data for i_rgb in self.to_rgb(hex_val)]
        except (ValueError, TypeError):
            return None
