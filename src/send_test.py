#!/usr/bin/env python
import logging, sys, os
from re import M
import pandas as pd
import json
from ast import literal_eval

from MQConnection import MQConnection

LOG_FORMAT = "%(levelname)-5s %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

if __name__ == "__main__":
    logger = logging.getLogger("main")
    logger.info("Question-Answer PolEval - Send test questions")

    file = open('testB.tsv')
    lines = file.readlines()
    
    class Collector:
        def __init__(self, size):
            self.results = []
            self.size = size

        def cb(self, channel, method, properties, body):
            answer = json.loads(literal_eval(str(body)).decode('utf8'))
            self.results.append(answer['answer'])
            channel.basic_ack(delivery_tag=method.delivery_tag)
            print(len(self.results), self.size)
            if len(self.results) == self.size:
                pd.DataFrame(self.results).to_csv('testB-results.tsv', header=None, index=None, sep=' ')
                exit(0)

    c = Collector(len(lines))
    print(c.size)
    mq = MQConnection()
    mq.connect(os.environ['MQURL'])
    mq.declare('questions')
    mq.register("answers", c.cb)

    for count, question in enumerate(lines):
        request = {
            'id': count,
            'question': question
        }
        mq.publish('questions', json.dumps(request))

    mq.spin()