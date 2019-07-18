from functools import lru_cache

solution = {}


@lru_cache(maxsize=2 ** 10)
def edit_distance(string1, string2):
    global solution
    if len(string1) == 0: return len(string2)
    if len(string2) == 0: return len(string1)

    tail_s1 = string1[-1]
    tail_s2 = string2[-1]
    a = (edit_distance(string1[:-1], string2) + 1, 'DEL {}'.format(tail_s1))
    b = (edit_distance(string1, string2[:-1]) + 1, 'ADD {}'.format(tail_s2))
    candidates = [
        a,  # string 1 delete tail
        b,  # string 1 add tail of string2
    ]

    if tail_s1 == tail_s2:
        c = edit_distance(string1[:-1], string2[:-1]) + 0
        both_forward = (c, '')
    else:
        d = edit_distance(string1[:-1], string2[:-1]) + 1
        both_forward = (d, 'SUB {} => {}'.format(tail_s1, tail_s2))

    candidates.append(both_forward)

    min_distance, operation = min(candidates, key=lambda x: x[0])

    solution[(string1, string2)] = operation

    return min_distance


def parse_solution(string1, string2):

    if not string1:
        return []

    k = (string1, string2)

    res = parse_solution(string1[:-1], string2) + [{k:solution[(string1, string2)]}]

    return res



string1 = 'be'
string2 = 'beg'
edit_distance(string1, string2)
for k, v in solution.items():
    print(k, ': ', v)

print(parse_solution(string1, string2))
