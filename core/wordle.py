#!/usr/bin/env python
import re
import numpy as np
from collections import Counter
from regex import Search








class Wordle:
    def __init__(self, filename) -> None:
        self._filenme = filename
        self.available_words = self.total_words = self.load_db(filename)
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
        return prob

    @property
    def search(self) -> str:
        return self._search

    @search.setter
    def search(self, val: str) -> bool:
        val = val.replace(" ", "")
        if len(val) != 5:
            raise ValueError("Search string must have a length of 5")
        self._search = re.compile(val.lower().replace(self._wildcard, "[a-z]"))
        return True

    def _validate_search(self, val: str) -> bool:
        val = val.replace(" ", "")
        if len(val) != 5:
            raise ValueError("Search string must have a length of 5")
        return re.compile(val.lower().replace(self._wildcard, "[a-z]"))

    def load_db(self, filename, *args, **kwargs) -> np.array:
        print(f"loading {filename}")
        return np.load(filename, *args, **kwargs)

    def get_possibilities(self, search, possible=[]) -> bool:
        new_possible = []
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
            _probability = self.get_probability(x)
            if _probability != 0:
                _prob_dist[x] = _probability
        self._last_prob_dist = sorted(
            _prob_dist.items(), key=lambda item: item[1], reverse=True
        )
        return self._last_prob_dist[:5]

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
        self.__init__(self._filenme)
        return True


w = Wordle("out.npy")
# w.get_possibilities()
