import spacy
from nltk.corpus import stopwords
import stanza
import spacy_stanza
import re
import functools
import operator

CONTENT_POS = ['ADJ','ADV','NOUN','PROPN','VERB']

## TODO change stanza on udpipe
## TODO adjust to many questions (remove loop in main)
## TODO 

class QuestionGenerator :

    def __init__(self):
        self.nlp_spacy = spacy.load("pl_core_news_sm")
        # nltk.download('stopwords')
        # stanza.download("pl")
        self.stopwords = set(stopwords.words('polish'))
        self.stanza_model = spacy_stanza.load_pipeline("pl")

    def generateQuestionAll(self, text):
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
        questions["pairsNA"] = self._extractNounAdj(doc)
        questions["pairsAN"] = self._extractAdjNoun(doc)
        questions['quotations'] = self._extractQuotation(text)
        questions['capitalLetters'] = self._extractCapitalLetters(text)
        return questions

    def generateQuestion(self, text,enable = ['keywords', 'stopwords', 'pairsAN', 'pairsNA', 'quotations', 'capitalLetters']):
        questions = {}
        if 'keywords' in enable :
            questions['keywords'] = self._extractKeywords(text)
        if 'stopwords_lemma' or 'stopwrods' or 'functional' or 'functional_lemma' in enable:
            doc = self.stanza_model(text)
        if 'stopwords_lemma' or 'stopwords' in enable :
            stopwords = self._extractQuestionWithoutStopwords(doc)
            if 'stopwords_lemma'in enable:
                questions['stopwords_lemma'] = [stopwords[0]]
            if 'stopwords' in enable:
                questions['stopwords'] = [stopwords[1]]
        if 'functional' or 'functional_lemma' in enable:
            functional = self._extractQuestionWithoutFunctionalWords(doc)
            if 'functional' in enable :
                questions['functional'] = [functional[0]]
            if 'functional_lemma' in enable :
                questions['functional_lemma'] =[functional[1]]
        if 'pairsAN' in enable :
            questions['pairsAN'] = self._extractAdjNoun(doc)
        if 'pairsNA' in enable :
            questions['pairsNA'] = self._extractNounAdj(doc)
        if 'quotations' in enable :
            questions['quotations'] =self._extractQuotation(text)
        if 'capitalLetters' in enable :
            questions['capitalLetters'] = self._extractCapitalLetters(text)
        #questions = functools.reduce(operator.iconcat, questions, [])
        return questions

        
    def _extractKeywords(self, text):
        doc = self.nlp_spacy(text)
        keyword = []
        for ent in doc.ents :
            keyword.append(str(ent))
        return keyword

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
    
    def _extractAdjNoun(self,doc):
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

    def _extractNounAdj(self,doc):
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
    
    def _extractQuotation(self, text):
        quotations = text.split('"')[1::2]
        return quotations


    def _extractCapitalLetters(self,text) :
        quot = []
        quots = []
        sentences = re.split('\. |\? ', text)
        for sentence in sentences :
            flag = False
            words = sentence.split(' ')
            for i,word in enumerate(words) :
                word = word.replace('.', '')
                word = word.replace('?', '')
                if len(word) :
                    if word[0].isupper() and i != 0 :
                        flag = True
                    elif flag and not word[0].isupper() :
                        quots.append(' '.join(quot))
                        flag = False
                    else :
                        flag = False
                    if flag :
                        quot.append(word)
        return quots



            

