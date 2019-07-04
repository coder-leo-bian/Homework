
import random
import numpy

defined_patterns = {
    "I need ?X": ["Image you will get ?X soon", "Why do you need ?X ?"],
    "My ?X told me something": ["Talk about more about your ?X", "How do you think about your ?X ?"]
}


def is_variable(pat):
    # 判断单个特殊字符 返回值：True / False
    return pat.startswith('?') and all(p.isalpha() for p in pat[1:])


#   i want ?y,  i want iphone 形式的匹配方式
def pattern_match(pattern, saying):
    # 返回匹配对象 [('?X', 'iphone')]
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


def pat_to_dict(pat_dict):
    # 根据匹配对象建立字典
    return {key: ' '.join(val) if isinstance(val, list) else val for key, val in pat_dict}


def subsitite(rule, parsed_rules):
    # 根据字典建立的规则和 字符串输出完整的句子
    if not rule: return []
    return [parsed_rules.get(rule[0], rule[0])] + subsitite(rule[1:], parsed_rules)


def is_pattern_segment(pat):
    # '?*X' 判断是否匹配多个字符，
    return pat.startswith('?*') and all(p.isalpha() for p in pat[2:])


def pat_match_with_seg(pattern, saying):
    # 返回匹配的规则
    if not pattern or not saying:
        return []
    pat = pattern[0]
    if is_variable(pat):
        return [(pat, saying[0])] + pat_match_with_seg(pattern[1:], saying[1:])
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    elif is_pattern_segment(pat):
        match, index = segment_match(pattern, saying)
        return [match] + pat_match_with_seg(pattern[1:], saying[index:])
    else:
        return False


def segment_match(pattern, saying):
    seg_pat, rest = pattern[0], pattern[1:]
    seg_pat = seg_pat.replace('?*', '?')

    if not rest: return (seg_pat, saying), len(saying)

    for i, token in enumerate(saying):
        if rest[0] == token and is_match(rest[1:], saying[(i + 1):]):
            return (seg_pat, saying[:i]), i

    return (seg_pat, saying), len(saying)


def is_match(rest, saying):
    if not rest and not saying:
        return True
    if not all(a.isalpha() for a in rest[0]):
        return True
    if rest[0] != saying[0]:
        return False
    return is_match(rest[1:], saying[1:])


# '?*P is very good'  , "My dog and my cat is very good"
# result = pat_match_with_seg('?*P is very good'.split(), "My dog and my cat is very good".split())
# print(result)


# def get_response(saying, rules):
#     for pat, values in rules.items():
#         if not pattern_match(pat.split(), saying.split()):
#             continue
#         parsed_rules = pat_to_dict(pattern_match(pat.split(), saying.split()))
#         subsitite_rule = random.choice(values)
#         res = subsitite(subsitite_rule.split(), parsed_rules)
#         if res:
#             return ' '.join(res)
#     return None


def get_response(saying, rules):
    for pat, values in rules.items():
        if not pat_match_with_seg(pat.split(), saying.split()):
            continue
        parsed_rules = pat_to_dict(pat_match_with_seg(pat.split(), saying.split()))
        subsitite_rule = random.choice(values)
        res = subsitite(subsitite_rule.split(), parsed_rules)
        if res:
            return ' '.join(res)
    return None


rules = {
    "?*X hello ?*Y": ["Hi, how do you do?"],
    "I was ?*X": ["Were you really ?X ?", "I already knew you were ?X ."]
}

res = get_response('I was ', rules)

print(res)
