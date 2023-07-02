import re


def to_camel_case(s):
    s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([s[0].lower(), s[1:]])


def camel_to_underscore(name):
    camel_pat = re.compile(r'([A-Z])')
    return camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)


def underscore_to_camel(name):
    under_pat = re.compile(r'_([a-z])')
    return under_pat.sub(lambda x: x.group(1).upper(), name)


def convert_json(data, convert):
    if isinstance(data, dict):
        new_d = {}

        for k, v in data.items():
            new_d[convert(k)] = convert_json(v, convert) if isinstance(v, dict) else convert_json(v, convert) if isinstance(v, list) else v

        return new_d
    elif isinstance(data, list):
        new_l = []

        for d in data:
            new_l.append(convert_json(d, convert))

        return new_l
