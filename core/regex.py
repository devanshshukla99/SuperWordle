import string


class Letter:
    def __init__(self, char="*") -> None:
        self._wildcard = "*"
        # self._wildcard_regex = "[a-z]"
        self._wildcard_regex = list(string.ascii_lowercase)
        self._fixed = False
        self._blacklist = set()
        self._regex = self._wildcard_regex
        return

    def __repr__(self):
        return self.regex

    def _process_wildcard(self):
        return self._regex.replace(
            self._wildcard, f'[{"|".join(self._wildcard_regex)}]'
        )

    @property
    def regex(self):
        if not self._fixed:
            self._regex = f'[{"|".join(self._wildcard_regex)}]'
        return self._regex

    def blacklist(self, val: str) -> bool:
        self._blacklist.add(val)
        self._wildcard_regex.remove(val)
        return True

    def _black_generate(self) -> str:
        if not self._blacklist:
            return ""
        _black = "|".join(self._blacklist)
        return f"(?![{_black}])"

    def fix(self, val: str) -> str:
        self._fixed = True
        self._regex = val

    pass


class Search:
    def __init__(self, wordlen=5) -> None:
        self._letters = [Letter("*") for _ in range(0, wordlen)]
        self._possibles = set()
        self._blacklist = set()

    def __repr__(self):
        return self.regex()

    def blacklist_all(self, chars: str) -> bool:
        for char in chars:
            self.blacklist("*", char)
        self._clear_dubs()
        return

    def blacklist(self, index, char) -> bool:
        if index == "*":
            self._blacklist.add(char)
            return
        self._letters[index].blacklist(char)
        self._possibles.add(char)
        return True

    def _clear_dubs(self, alpha_freq=None) -> bool:
        self._blacklist = self._blacklist.difference(self._possibles)
        for x in self._blacklist:
            if alpha_freq:
                if x in alpha_freq:
                    alpha_freq.pop(x)
            for _l in self._letters:
                _l.blacklist(x)
        return True

    def validate_possibles(self, word):
        for i in self._possibles:
            if i not in word:
                return False
        return True

    def fix(self, index, char) -> bool:
        self._letters[index].fix(char)
        self._possibles.add(char)
        return True

    def regex(self):
        _regex = "".join([x.regex for x in self._letters])
        return "".join(["^", _regex])

    def _import(self, induct) -> str:
        for idx, x in enumerate(induct):
            self._letters[idx]._fixed = x.get("fixed")
            self._letters[idx]._blacklist = x.get("blacklist")
            if x.get("fixed"):
                self._letters[idx]._regex = x.get("regex")
            assert self._letters[idx].regex == x.get("regex")

    def _export(self) -> str:
        return [
            {
                "fixed": x._fixed,
                "blacklist": x._blacklist,
                "regex": x.regex,
            }
            for x in self._letters
        ]

    def reset(self) -> str:
        self.__init__()

    pass
