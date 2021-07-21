#!/usr/bin/env python
import logging
from MQConnection import MQConnection

LOG_FORMAT = "%(levelname)-5s %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

if __name__ == "__main__":
    logger = logging.getLogger("main")
    logger.info("Hello world!")

    mq = MQConnection()
    mq.connect('amqp://localhost:5672/%2f')
    mq.stop()
