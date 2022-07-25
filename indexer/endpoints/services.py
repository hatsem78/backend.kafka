import os

from kafka import KafkaConsumer
import json
from fastapi import APIRouter, HTTPException, Depends
from kafka import KafkaConsumer
from sqlalchemy.orm.session import Session
import asyncio
from core.settings import config
from core.settings import get_logger
from db.crud import crud_auto

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
DETECTIONS_TOPIC = os.environ.get("DETECTIONS_TOPIC")
logger = get_logger('endpoints items')
logger.getChild('endpoints service consumer')


def consumer(filter, db):
    result = None

    '''consumer = KafkaConsumer(
        DETECTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        group_id='Pickup'
    )

    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))
        if isinstance(message.value, bytes): 
            result = message.value.decode()
        else:
            result = message.value.decode()'''

    consumer = KafkaConsumer(
        DETECTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        group_id='Pickup'
    )

    logger.info(
        f"Start consumer with  topic '{config.DETECTIONS_TOPIC}'."
    )

    logger.info("Consumer started.")

    try:

        logger.info(f"Get {len(result)} messages in {config.DETECTIONS_TOPIC}.")

        for message in consumer:

            if isinstance(message.key, bytes):
                result = message.key.decode()
            else:
                result = message.key.decode()
            if result == filter:
                crud_auto.token.create(db=db, obj_in=message.value.decode())
                return message.value.decode()
    except Exception as e:
        logger.error(
            f"Error when trying to consume request for topic {config.DETECTIONS_TOPIC}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=str(e))

    return None
