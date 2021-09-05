import logging, sys, os
from Keywords.QuestionGenerator import QuestionGenerator
from MQConnection import MQConnection
from Document import Elastic, Document
from ast import literal_eval
import json
from QAModel.AnswersReplier import AnswersReplier
LOG_FORMAT = "%(levelname)-5s %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class Controller :
    def __init__ (self) :
        self.mq = MQConnection()
        self.mq_pub = MQConnection()
        self.qa = QuestionGenerator()
        self.ar = AnswersReplier()
        self.logger = logging.getLogger("main")
        self.logger.info("Connecting to MQ")
        self.mq.connect(os.environ['MQURL'])
        self.mq_pub.connect(os.environ['MQURL'])
        print({ 'host': os.environ['ESHOST'], 'port': int(os.environ['ESPORT']) })
        self.es = Elastic({ 'host': os.environ['ESHOST'], 'port': int(os.environ['ESPORT']) }, 'poleval')
        self.generated_questions = {}
        self.documents = []
        self.responses = []
    
    def callback_questionGenerator(self, ch, method, properties, body):
        try:
            question = json.loads(literal_eval(str(body)).decode('utf8'))
            self.logger.info(f"Received {question}")
            self.generated_questions = self.qa.generateQuestion(question['question'])
            self.logger.info(f"Generated questions {self.generated_questions}")
            self.get_documents()
            best_answer = self.ar.get_best_answer(documents=self.documents, question=question['question'])
            self.logger.info(f"Answer {best_answer}")
            response = {
                'id': question['id'],
                'question': question['question'],
                'answer': best_answer['answer']
            }
        except:
            response = {
                'id': question['id'],
                'question': question['question'],
                'answer': 'Tak'
            }
        finally:
            try:
                self.mq.channel.basic_ack(delivery_tag=method.delivery_tag)
                self.mq_pub.publish(queue='answers', body=json.dumps(response))
                print(json.dumps(response))
            except:
                pass

    def publish(self, queue, body):
        self.mq.publish(queue, body)
        
    def callback_elasticSearch(self, ch, method, properties, body):
        self.logger.info(f"Received {literal_eval(str(body)).decode('utf8')}")

    def register_replier_queue(self):
        self.mq.register("questions", self.callback_questionGenerator)
    
    def register_answers_queue(self):
        self.mq_pub.declare('answers')
        # self.mq_pub.register("answers", self.callback_elasticSearch)
    
    def get_generated_question(self):
        return self.generated_questions

    def get_documents(self):
        self.documents = []
        document_map = {}
        for queries in self.generated_questions.values():
            for query in queries:
                docs = self.es.get(query)
                for doc in docs:
                    document_map[doc.id] = doc
        self.documents = list(document_map.values())
        return self.documents

    def spin(self):
        self.mq.spin()
    
    def stop(self):
        self.mq.stop()

    