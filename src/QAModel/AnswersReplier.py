
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
        #print(context)
        output = self.qa_pipeline({
                    'context': context,
                    'question': question
                    })
        AnswersReplier.logger.info(f"[Q]: {question} \n [A]: {output['answer']} \n [score]: {output['score']}")
        return output

    def split_documents2contexts(self, documents):
        contexts = []
        i = 0
        max_docs = min(15, len(documents)) ## some param..?
        while i < max_docs:
            #contexts.append(documents[i].abstract)
            ##TODO: split text into smaller pieces 
            contexts.append(documents[i].text)
            i+=1
        return contexts

    def get_answers(self, question, contexts):
        outputs = []
        for context in contexts:
            if context is not None:
                output = self.getAnswer(question, context)
                outputs.append(output)
        return outputs

    def get_best_answer(self, documents, question):
        contexts = self.split_documents2contexts(documents)
        outputs = self.get_answers(question, contexts)
        best_answer = max(outputs, key=lambda output: output['score'])
        return best_answer