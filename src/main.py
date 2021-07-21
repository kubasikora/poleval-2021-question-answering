#!/usr/bin/env python
import logging, sys, os
from MQConnection import MQConnection

LOG_FORMAT = "%(levelname)-5s %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

if __name__ == "__main__":
    logger = logging.getLogger("main")
    logger.info("Hello world!")

    mq = MQConnection()
    mq.connect(os.environ['MQURL'])
    mq.register("hello", lambda channel, method, properties, body: logger.info(f"Received {str(body)}"))

    try:
        mq.spin()
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            mq.stop()
            sys.exit(0)
        except SystemExit:
            os._exit(0)
