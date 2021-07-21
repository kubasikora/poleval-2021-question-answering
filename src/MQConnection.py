import pika
import logging

class MQConnection:
    logger = logging.getLogger("MQConnection")
    
    def __init__(self) -> None:
        self.connection = None
        self.url = None

    def connect(self, url) -> None:
        if self.url is not None:
            self.stop()
        self.connection = pika.BlockingConnection(parameters=pika.URLParameters(url))
        self.url        = url
        self.channel    = self.connection.channel()
        MQConnection.logger.info(f"Connected to {self.url}")

    def stop(self) -> None:
        self.connection.close()
        MQConnection.logger.info("Stopped connection")

    def register(self, queue, callback) -> None:
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        MQConnection.logger.info(f"Registered consumer to queue {queue}")

    def spin(self) -> None:
        MQConnection.logger.info("Waiting for messages")
        self.channel.start_consuming()
