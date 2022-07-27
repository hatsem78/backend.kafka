import asyncio
import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from core.settings import get_logger
from db.auth import get_db
from endpoints.services import consumer

router = APIRouter()
logger = get_logger('endpoints items')
logger.getChild('endpoints items')

loop = asyncio.get_event_loop()


def kafka_json_deserializer(serialized):
    return json.loads(serialized)


@router.post("/{group_id}")
async def read_item(group_id: str, db: Session = Depends(get_db)):
    """
    Consume a list of 'Requests' from 'KAFKA_BROKER_URL'.
    """

    await consumer(group_id, db)

    return "hola"
