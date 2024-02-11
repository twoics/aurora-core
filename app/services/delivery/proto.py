import typing


@typing.runtime_checkable
class Delivery(typing.Protocol):
    async def send(self, to: str, message: typing.List[int]):
        ...
