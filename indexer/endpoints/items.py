import json
from fastapi import APIRouter, HTTPException, Depends
from kafka import KafkaConsumer
from sqlalchemy.orm.session import Session
import asyncio
from core.settings import config
from core.settings import get_logger
from db.auth import get_db
from db.crud import crud_auto
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

    consumer(group_id, db)

    return "hola"


