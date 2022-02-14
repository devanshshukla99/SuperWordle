#!/usr/bin/env python
import re
import pandas as pd
import numpy as np
from collections import Counter


def sanatize_db(filename, out="only_5.wordlist", header=None, delimiter=",") -> bool:
    df = pd.read_csv(filename, header=header, delimiter=delimiter)
    df2 = [df[0][x] for x in range(len(df[0])) if len(str(df[0][x])) == 5]
    df2 = np.array(df2)
    np.save(out, df2)
    return True


class Wordle:
    def __init__(self) -> None:
        self.available_words = self.total_words = self.load_db()
        self._total_alpha = 0
        self._get_total_alphabets()
        self._blacklist = set()
        self._search = ""
        self._wildcard = "*"

    def _get_total_alphabets(self):
        self.alpha_counter = Counter()
        for x in self.available_words:
            alphas = re.findall("[a-z]", x)
            self.alpha_counter.update(alphas)
        self._total_alpha = sum(self.alpha_counter.values())
        return True

    def get_probability(self, word):
        word = word.lower()
        alpha = re.findall("[a-z]", word)
        prob = 0
        for c in alpha:
            _p = self.alpha_counter.get(c)
            if not _p:
                return 0
            prob += _p / self._total_alpha
            print(_p, f"{_p / self._total_alpha}")
        return prob

    @property
    def search(self) -> str:
        return self._search

    @search.setter
    def search(self, val: str) -> bool:
        val = val.replace(" ", "")
        if len(val) != 5:
            raise ValueError("Search string must have a length of 5")
        print(val)
        self._search = re.compile(val.lower().replace(self._wildcard, "[a-z]"))
        return True

    def _validate_search(self, val: str) -> bool:
        val = val.replace(" ", "")
        if len(val) != 5:
            raise ValueError("Search string must have a length of 5")
        print(val)
        return re.compile(val.lower().replace(self._wildcard, "[a-z]"))

    def load_db(self, filename="only_5.wordlist.npy", *args, **kwargs) -> np.array:
        return np.load(filename, *args, **kwargs)

    def get_possibilities(self, search, possible=[]) -> bool:
        new_possible = []
        print(possible)
        for x in self.available_words:
            check = search.fullmatch(x)
            if check:
                assert x == check.group()
                if possible:
                    for y in possible:
                        if y in x:
                            if x not in new_possible:
                                new_possible.append(x)
                else:
                    new_possible.append(check.group())
        return np.array(new_possible)

    def suggest(self, search: str = "*****", possible: str = ""):
        self.available_words = self.get_possibilities(
            self._validate_search(search), list(possible)
        )
        _prob_dist = {}
        for x in self.available_words:
            _prob_dist[x] = self.get_probability(x)
        self._last_prob_dist = sorted(_prob_dist.items(), key=lambda item: item[1])
        return self._last_prob_dist[-1], self._last_prob_dist[-2]

    def blacklist(self, black):
        self._blacklist = self._blacklist.union(list(black))
        for x in self._blacklist:
            _ = self.alpha_counter.pop(x, False)

    def update(self, guess, possible=None):
        _guess = guess
        if possible:
            for x in list(possible):
                _guess = _guess.replace(x, "")
        self.blacklist(list(_guess))
        return True

    def reset(self) -> bool:
        self.__init__()
        return True


w = Wordle()
# w.get_possibilities()
