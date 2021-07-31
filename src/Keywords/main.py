from QuestionGenerator import QuestionGenerator
import pandas as pd

if __name__ == "__main__":
    qa = QuestionGenerator()

    df = pd.read_csv('src/Keywords/QA.csv')
    questions = df["Question"].to_list()

    dictqa = []
    for question in questions :
        dictqa.append( qa.generateQuestion(question) )
    
    df_qa = pd.DataFrame.from_dict(dictqa)
    df_qa.to_csv('QA_post.csv')
        


    