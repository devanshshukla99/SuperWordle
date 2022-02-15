import re
import numpy as np
from collections import Counter

# coun = Counter()
total_alphabets = 0
alphabets = re.findall("[a-z]", self.total_words)
total_alphabets += len(alphabets)

# coun.update(alphabets)








def replace_wildcard(search):
    return search.replace("*", "[a-z]")

def replace_elsewhere(search):
    match = re.search(r"#[a-z]", search)
    if match:
        grp = match.group()
        char = grp[-1]
        return "^" + search.replace(grp, f"(?!{char})[a-z]")
    return "^" + search

def parse_search(search):
    search = replace_wildcard(search)
    return re.compile(replace_elsewhere(search))

def probability(search):
    words = np.load("out.npy")
    total_words = len(words)
    search = "**r*#s"
    regex = parse_search(search)

    _possible = get_possibilities(regex)
    _prob = len(_possible) / total_words
    print(_prob)
    info = -np.log2(_prob)
    print(f"{info} bits")

def get_possibilities(regex, available_words) -> bool:
    new_possible = list(filter(regex.match, available_words))
    return new_possible



    # for x in words:
    #     check = search.fullmatch(x)
    #     if check:
    #         assert x == check.group()
    #         if possible:
    #             for y in possible:
    #                 if y in x:
    #                     if x not in new_possible:
    #                         new_possible.append(x)
    #         else:
    #             new_possible.append(check.group())
    # return np.array(new_possible)

    