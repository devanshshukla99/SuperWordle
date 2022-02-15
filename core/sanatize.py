import pandas as pd
import numpy as np


def sanatize_db(
    filename,
    out="only_5.wordlist",
    wordlen=5,
    header=None,
    delimiter=",",
) -> bool:
    df = pd.read_csv(filename, header=header, delimiter=delimiter)
    df2 = [df[0][x] for x in range(len(df[0])) if len(str(df[0][x])) == wordlen]
    df2 = np.array(df2)
    np.save(out, df2)
    return True


out = []
for i in nltk.corpus.brown.tagged_words():
    if len(i[0]) == 5:
        out.append(i)
words = [x[0].lower() for x in out]
np.save("out", np.array(words))
