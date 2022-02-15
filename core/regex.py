class Letter:
    def __init__(self, char="*") -> None:
        self._wildcard = "*"
        self._wildcard_regex = "[a-z]"
        self._fixed = False
        self._blacklist = []
        self._regex = self._wildcard_regex
        return

    def __repr__(self):
        return self.regex

    def _process_wildcard(self):
        return self._regex.replace(self._wildcard, self._wildcard_regex)

    @property
    def regex(self):
        if not self._fixed:
            self._regex = "".join([self._black_generate(), self._wildcard_regex])
        return self._regex

    def blacklist(self, val: str) -> bool:
        self._blacklist.append(val)

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

    def blacklist(self, index, char) -> bool:
        self._letters[index].blacklist(char)
        return True

    def regex(self):
        _regex = "".join([x.regex for x in self._letters])
        return "".join(["^", _regex])

    pass
