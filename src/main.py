#!/usr/bin/env python
import logging, sys, os
from Controller import Controller
import pandas as pd

LOG_FORMAT = "%(levelname)-5s %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def callback(ch, method, properties, body):
    logger.info(f"Received {str(body)}")


if __name__ == "__main__":
    logger = logging.getLogger("main")
    logger.info("Question-Answer PolEval")

    controller = Controller()
    controller.register_replier_queue()
    controller.register_answers_queue()

    try:
        controller.spin()
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            pd.DataFrame(controller.results).to_csv("./results.tsv")
            controller.stop()
            sys.exit(0)
        except SystemExit:
            os._exit(0)
