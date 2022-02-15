#!/usr/bin/env python
import re
import numpy as np
from collections import Counter
from core.regex import Search
from rich.progress import track


class Wordle:
    def __init__(self, filename) -> None:
        self._filenme = filename
        self._raw = self._load_db(filename)
        self.total_words = [x[0] for x in self._raw]
        self.available_words = self.total_words
        self._total_alphas, self._alpha_freq = self._get_total_alphabets(
            self.available_words
        )
        self._blacklist = set()
        self._search = Search()
        return

    def __repr__(self):
        return f"<{self.__class__.__name__} [search:{self._search}] [total words:{len(self.total_words)}] [total chars:{self._total_alphas}]>"

    def _load_db(self, filename, *args, **kwargs) -> np.array:
        print(f"loading {filename}")
        return np.load(filename, *args, **kwargs)

    def _get_total_alphabets(self, words):
        _alpha_counter = Counter()
        for x in words:
            _alpha_counter.update(list(x))
        return sum(_alpha_counter.values()), _alpha_counter

    def probability(self, word):
        word = word.lower()
        prob = 0
        for c in list(word):
            _p = self._alpha_freq.get(c)
            if not _p:
                return 0
            prob += _p / self._total_alphas
        return round(prob, 4)

    def retrive_possibles(self, pattern, available_words) -> bool:
        regex = re.compile(pattern)
        possibles = list(filter(regex.match, available_words))
        # print(possibles)
        new_possibles = [x for x in possibles if self._search.validate_possibles(x)]
        # print(new_possibles)
        return new_possibles

    def blacklist(self, index, char):
        self._search.blacklist(index, char)

    def _parse_previous_guess(self, previous_guess, pattern: str):
        pattern = list(pattern)
        print(previous_guess, pattern)
        for idx, p in enumerate(pattern):
            if p == "*":
                self.blacklist("*", previous_guess[idx])
            else:
                if p == "#":  # blacklist/exclude
                    self.blacklist(idx, previous_guess[idx])
                else:  # fix
                    self._search.fix(idx, p)
        self._search._clear_dubs(self._alpha_freq)
        return True

    def _entropy(self, possibles):
        _prob = len(possibles) / len(self.available_words)
        info = -np.log2(_prob)
        print(f"{info} bits")
        return info

    def _entropy_of_guesses(self, guesses):
        guess_info = []
        pattern = Search()
        for guess in track(guesses):
            # pattern._import(self._search._export())
            pattern.reset()
            pattern.blacklist_all(guess)
            regex = re.compile(pattern.regex())

            guess_possibles = list(filter(regex.match, self.available_words))

            info = -np.log2(len(guess_possibles) / len(self.available_words))
            guess_info.append((guess, round(info, 4)))
        return sorted(guess_info, key=lambda item: item[1], reverse=True)

    def _prob_by_freq(self, possibles):
        _prob_dist = {}
        for x in possibles:
            _probability = self.probability(x)
            if _probability != 0:
                _prob_dist[x] = _probability
        self._last_prob_dist = sorted(
            _prob_dist.items(), key=lambda item: item[1], reverse=True
        )
        return

    def suggest(self, previous_guess=None, result_pattern=None):
        if result_pattern:
            self._parse_previous_guess(previous_guess, result_pattern)
        possibles = self.retrive_possibles(self._search.regex(), self.available_words)
        info = self._entropy(possibles)
        # self._prob_by_freq(possibles)
        guess_info = self._entropy_of_guesses(possibles)
        self.available_words = possibles
        return info, guess_info

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
