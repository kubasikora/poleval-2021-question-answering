
from AnswersReplier import AnswersReplier


TEST_QA = [

    {
        'context': "Warszawa jest największym miastem w Polsce pod względem liczby ludności i powierzchni",
        'question': "Jakie jest największe miasto w Polsce?"
    },
    {
        "context": "Normanowie (Norman: Nourmands; francuski: Normands; łac.: Normanni) byli ludźmi, którzy w X i XI wieku dali swoją nazwę Normandii, regionowi we Francji.  Wywodzili się oni z nordyckich (\"Norman\" pochodzi od \"Norseman\") najeźdźców i piratów z Danii, Islandii i Norwegii, którzy pod wodzą Rollo zgodzili się złożyć przysięgę wierności królowi Karolowi III z Zachodniej Francji.  Poprzez pokolenia asymilacji i mieszania się z rdzenną ludnością frankijską i rzymsko-galicyjską, ich potomkowie stopniowo łączyli się z karolińskimi kulturami zachodniej Francji.  Odrębna kulturowa i etniczna tożsamość Normanów wyłoniła się początkowo w pierwszej połowie X wieku, a następnie ewoluowała przez kolejne stulecia.",
        "question": "W jakim kraju położona jest Normandia?"
    },
    {   "context": "Normanowie (Norman: Nourmands; francuski: Normands; łac.: Normanni) byli ludźmi, którzy w X i XI wieku dali swoją nazwę Normandii, regionowi we Francji.  Wywodzili się oni z nordyckich (\"Norman\" pochodzi od \"Norseman\") najeźdźców i piratów z Danii, Islandii i Norwegii, którzy pod wodzą Rollo zgodzili się złożyć przysięgę wierności królowi Karolowi III z Zachodniej Francji.  Poprzez pokolenia asymilacji i mieszania się z rdzenną ludnością frankijską i rzymsko-galicyjską, ich potomkowie stopniowo łączyli się z karolińskimi kulturami zachodniej Francji.  Odrębna kulturowa i etniczna tożsamość Normanów wyłoniła się początkowo w pierwszej połowie X wieku, a następnie ewoluowała przez kolejne stulecia.",
        "question": "Z jakich krajów wywodzili się Norwedzy?"
    }
]
if __name__ == "__main__":
    ar = AnswersReplier()
    for qa in TEST_QA:
        resp = ar.getAnswer(question = qa['question'], context = qa['context'])
