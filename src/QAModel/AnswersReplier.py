
import logging
import sys
from transformers import pipeline

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

class AnswersReplier:

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    logger = logging.getLogger('QA')
    logger.setLevel(logging.DEBUG) # better to have too much log than not enough
    logger.addHandler(console_handler)

    def __init__(self, modelName = "henryk") -> None:
        AnswersReplier.logger.info("AnswersReplier module init")
        self.modelName = modelName
        AnswersReplier.logger.info(f"Model {self.modelName} loading...")

        if self.modelName == "henryk":
            self.qa_pipeline = pipeline(
                "question-answering",
                model="henryk/bert-base-multilingual-cased-finetuned-polish-squad2",
                tokenizer="henryk/bert-base-multilingual-cased-finetuned-polish-squad2"
            )

        else: 
            AnswersReplier.logger.warning("No such model")
            return
        AnswersReplier.logger.info(f"Model {self.modelName} loaded.")

    
    def getAnswer(self, question, context):
        output = self.qa_pipeline({
                    'context': context,
                    'question': question
                    })
        print(output)
        AnswersReplier.logger.info(f"[Q]: {question} \n [A]: {output['answer']} \n [score]: {output['score']}")
        return output