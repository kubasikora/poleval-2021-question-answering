import spacy
from nltk.corpus import stopwords
import stanza
import spacy_stanza

CONTENT_POS = ['ADJ','ADV','NOUN','PROPN','VERB']

class QuestionGenerator :

    def __init__(self):
        self.nlp_spacy = spacy.load("pl_core_news_sm")
        # nltk.download('stopwords')
        # stanza.download("pl")
        self.stopwords = set(stopwords.words('polish'))
        self.stanza_model = spacy_stanza.load_pipeline("pl")

    def generateQuestion(self, text):
        questions = {}
        questions['question'] = text
        questions["keywords"] = self._extractKeywords(text)
        doc = self.stanza_model(text)
        stopwords = self._extractQuestionWithoutStopwords(doc)
        questions["stopwords_lemma"] = stopwords[0]
        questions["stopwords"] = stopwords[1]
        functional = self._extractQuestionWithoutFunctionalWords(doc)
        questions["functional"] = functional[0]
        questions["functional_lemma"] = functional[1]
        questions["pairsAN"] = self._extractNounAdj(doc)
        questions["pairsNA"] = self._extractAdjNoun(doc)
        return questions

    def _extractKeywords(self, text):
        doc = self.nlp_spacy(text)
        return doc.ents

    def _extractQuestionWithoutStopwords(self,doc):
        tokens_lemma = []
        tokens =[]
        for token in doc:
            if token.text.lower() not in self.stopwords and token.pos_ != 'PUNCT':
                tokens_lemma.append(token.lemma_)
                tokens.append(token.text)
        tokens_text_lemma = ' '.join(tokens_lemma)
        tokens_text = ' '.join(tokens)
        return [tokens_text_lemma, tokens_text]
    
    def _extractQuestionWithoutFunctionalWords(self,doc):
        tokens = []
        tokens_lemma = []
        for token in doc:
            if token.pos_ in CONTENT_POS:
                tokens_lemma.append(token.lemma_)
                tokens.append(token.text)
        tokens_text = ' '.join(tokens)
        tokens_text_lemma = ' '.join(tokens_lemma)
        return [tokens_text, tokens_text_lemma]
    
    def _extractNounAdj(self,doc):
        tokens = []
        flag = False
        for i,token in enumerate(doc):
            if token.pos_ in ['ADV', 'ADJ']:
                flag = True
            elif flag and token.pos_ == 'NOUN':
                tokens.append(' '.join([doc[i-1].text, token.text]))
                flag = False
            else :
                flag = False
        return tokens

    def _extractAdjNoun(self,doc):
        tokens = []
        flag = False
        for i,token in enumerate(doc):
            if token.pos_ == 'NOUN':
                flag = True
            elif flag and token.pos_ in ['ADV', 'ADJ']:
                tokens.append(' '.join([doc[i-1].text, token.text]))
                flag = False
            else :
                flag = False
        return tokens


            

