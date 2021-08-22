import logging, sys, os
from Keywords.QuestionGenerator import QuestionGenerator
from MQConnection import MQConnection
from ast import literal_eval

LOG_FORMAT = "%(levelname)-5s %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class Controller :
    def __init__ (self) :
        self.mq = MQConnection()
        self.qa = QuestionGenerator()
        self.logger = logging.getLogger("main")
        self.logger.info("Connecting to MQ")
        self.mq.connect(os.environ['MQURL'])
        self.generated_questions = {}   
    
    def callback_questionGenerator(self,ch, method, properties, body):
        self.logger.info(f"Received {literal_eval(str(body)).decode('utf8')}")
        self.generated_questions = self.qa.generateQuestion(literal_eval(str(body)).decode('utf8'))
        self.logger.info(f"Generated questions {self.generated_questions}")

    def register(self, task = "questionGenrator"):
        self.mq.register("questionGenerator", self.callback_questionGenerator)
    
    def spin(self):
        self.mq.spin()
    
    def stop(self):
        self.mq.stop()