#!/usr/bin/env python
import logging, sys, os
from Controller import Controller

LOG_FORMAT = "%(levelname)-5s %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

if __name__ == "__main__":
    logger = logging.getLogger("main")
    logger.info("Question-Answer PolEval - Send test questions")

    file = open('devA.tsv')
    lines = file.readlines()

    controller = Controller()
    controller.register_question_generator()

    for line in lines:
        controller.publish('questionGenerator', line)