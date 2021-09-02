#!/usr/bin/env python
import logging, sys, os
from Controller import Controller

LOG_FORMAT = "%(levelname)-5s %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def callback(ch, method, properties, body):
    logger.info(f"Received {str(body)}")


if __name__ == "__main__":
    logger = logging.getLogger("main")
    logger.info("Question-Answer PolEval")

    controller = Controller()
    controller.register_question_generator()
    controller.register_elastic_search()

    try:
        controller.spin()
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            controller.stop()
            sys.exit(0)
        except SystemExit:
            os._exit(0)
