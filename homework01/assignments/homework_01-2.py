
import random

defined_patterns = {
    "I need ?X": ["Image you will get ?X soon", "Why do you need ?X ?"],
    "My ?X told me something": ["Talk about more about your ?X", "How do you think about your ?X ?"]
}


# 1.判断两个语句是否相符，并输出特殊字符对应的词 i want ?X，  i want iphone (?X --- iphone)
def is_variable(pat):
    return pat.startswith('?') and all(p.isalpha() for p in pat[1:])


# 2. ?x i want ?y 形式的匹配方式
def pattern_match(pattern, saying):
    if not pattern or not saying: return []
    if is_variable(pattern[0]):
        a = [(pattern[0], saying[0])]
        b = pattern_match(pattern[1:], saying[1:]) if len(pattern) > 1 and len(saying) > 1 else []
        return a + b
    else:
        if pattern[0] != saying[0]:
            return False
        else:
            return pattern_match(pattern[1:], saying[1:])


# 3. 利用匹配的变量，并输出语句
def pat_to_dict(pat_dict):
    return {key: val for key, val in pat_dict}


def subsitite(rule, parsed_rules):
    if not rule: return []
    return [parsed_rules.get(rule[0], rule[0])] + subsitite(rule[1:], parsed_rules)


def get_response(saying, rules):
    for pat, values in rules.items():
        if not pattern_match(pat.split(), saying.split()):
            continue
        parsed_rules = pat_to_dict(pattern_match(pat.split(), saying.split()))
        subsitite_rule = random.choice(values)
        res = subsitite(subsitite_rule.split(), parsed_rules)
        if res:
            return ' '.join(res)
    return None


def is_pattern_segment(pat):
    return pat.startswith('?*') and all(p.isalpha() for p in pat[2:])

"""
'?*P is very good'  , "My dog and my cat is very good"
"""

def pattern_many(pattern, saying):
    res = []
    i, j = -1, -1
    data = []
    for index, pat in enumerate(pattern):
        if is_pattern_segment(pat):
            if i == -1:
                i = index
                p = pat
            else:
                res.append((p, data))
                data = []
                i = index
                p = pat
        else:
            data = pattern[i+1: index+1]
    res.append((p, data))
    start = 0
    for d in res:
        length = len(d[1])
        for i in range(len(saying)-length+1):
            if d[1] == saying[i: length+i]:
                print(d[0], '--->', saying[start: i])
                start = length + i


pattern_many('?*P is very good ?*Y abvc ?*Z e'.split(), "My dog and my cat is very good a b c d abvc abc d e".split())


#
# res = get_response('My son told me something', defined_patterns)
#
# print(res)
