from config.config import Settings
from deps.config import get_settings
from deps.delivery import get_delivery
from deps.repo import get_client_repo
from deps.repo import get_matrix_repo
from deps.repo import get_user_repo
from fastapi import Depends
from repo.client.proto import ClientRepo
from repo.matrix.proto import MatrixRepo
from repo.user.proto import UserRepo
from services.auth.tokens import TokenAuth
from services.connection.agent import ConnectionAgent
from services.connection.sender import DataSender
from services.delivery.proto import Delivery
from starlette.websockets import WebSocket


def get_connection_agent(
    websocket: WebSocket,
    uuid: str,
    matrix_repo: MatrixRepo = Depends(get_matrix_repo),
    client_repo: ClientRepo = Depends(get_client_repo),
    user_repo: UserRepo = Depends(get_user_repo),
    config: Settings = Depends(get_settings),
) -> ConnectionAgent:
    """Get connection agent for validate incoming websocket connection"""

    return ConnectionAgent(
        websocket=websocket,
        matrix_uuid=uuid,
        matrix_repo=matrix_repo,
        client_repo=client_repo,
        auth_service=TokenAuth(config),
        user_repo=user_repo,
    )


def get_data_sender(
    websocket: WebSocket,
    delivery: Delivery = Depends(get_delivery),
):
    """Get data sender for send data to matrix"""

    return DataSender(websocket=websocket, delivery=delivery)
