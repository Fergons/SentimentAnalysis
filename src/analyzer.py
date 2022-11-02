import pandas as pd
from flair.data import Sentence, Corpus

def test():
    model_name = "ufal/robeczech-base"
    sentence = Sentence("Hra super člově u ní dobře vypne, ale jen když pominu ty momenty, kdy se na vás vrhne celý tým, hra mě osobně hrozně moc baví, a každému bych jí jen doporučil, ale samozřejmě každý má vlastní vázor.")
    for t in sentence:
        print(t)

if __name__ == '__main__':
    test()

