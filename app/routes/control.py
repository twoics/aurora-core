from deps.connection import get_connection_agent
from deps.connection import get_data_receiver
from deps.connection import get_data_sender
from deps.connection import get_observer_factory
from fastapi import APIRouter
from fastapi import Depends
from services.connection.agent import ConnectionAgent
from services.connection.observer import ObserverFactory
from services.connection.receiver import DataReceiver
from services.connection.sender import DataSender

router = APIRouter()


@router.websocket('/{uuid}')
async def remote_control(
    agent: ConnectionAgent = Depends(get_connection_agent),
    observer_factory: ObserverFactory = Depends(get_observer_factory),
    receiver: DataReceiver = Depends(get_data_receiver),
    sender: DataSender = Depends(get_data_sender),
):
    """Matrix Remote control"""

    session = await agent.accept()
    observer = observer_factory.get_observer(session)

    async with observer as connection_observer:
        while True:
            data_to_send = await receiver.receive(session)
            await connection_observer.inspect_user()
            await sender.send(session, data_to_send)
