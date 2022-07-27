import asyncio
import os
from json import loads

from fastapi import HTTPException
from kafka import KafkaConsumer

from core.settings import config
from core.settings import get_logger
from db.crud import crud_auto

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
DETECTIONS_TOPIC = os.environ.get("DETECTIONS_TOPIC")
logger = get_logger('endpoints items')
logger.getChild('endpoints service consumer')


async def consumer(filters: object, db: object) -> object:
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

    consumer_app = KafkaConsumer(
        DETECTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        group_id=filters,
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    logger.info(
        f"Start consumer_app with  topic '{config.DETECTIONS_TOPIC}'."
    )

    logger.info("consumer_app started.")

    try:

        #logger.info(f"Get {len(result)} messages in {config.DETECTIONS_TOPIC}.")

        for message in consumer_app:

            if isinstance(message.key, bytes):
                result = message.key.decode()
            else:
                result = message.key.decode()
            if result == filters:
                message_new = {k.lower(): v for k, v in message.value.items()}
                crud_auto.crud_auto.create(db=db, obj_in=message_new)

    except Exception as e:
        logger.error(
            f"Error when trying to consume request for topic {config.DETECTIONS_TOPIC}: {str(e)}"
        )
        logger.error(e)
        consumer.pause()
        await asyncio.sleep(2)
        consumer.resume()
        raise HTTPException(status_code=500, detail=str(e))


    return None
