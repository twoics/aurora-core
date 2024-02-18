import typing


@typing.runtime_checkable
class Delivery(typing.Protocol):
    async def send(self, receiver_uuid: str, message: typing.List[int]):
        """Sends message to matrix with receiver uuid"""
