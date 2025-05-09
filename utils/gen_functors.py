import re
from pathlib import Path
from collections import defaultdict
from typing import Sized

from pandas.core.computation.ops import isnumeric
from scripts.regsetup import examples

functor_re = re.compile(r'\w+\([^\s\;]*\)')

paths = [
    Path(
        r'C:\Users\slafniy\Desktop\bg3modding\bg3-modders-multitool\UnpackedData\Gustav\Public\Gustav\Stats\Generated\Data'),
    Path(
        r'C:\Users\slafniy\Desktop\bg3modding\bg3-modders-multitool\UnpackedData\Gustav\Public\Honour\Stats\Generated\Data'),
    Path(
        r'C:\Users\slafniy\Desktop\bg3modding\bg3-modders-multitool\UnpackedData\Gustav\Public\GustavDev\Stats\Generated\Data'),
    Path(
        r'C:\Users\slafniy\Desktop\bg3modding\bg3-modders-multitool\UnpackedData\Shared\Public\Shared\Stats\Generated\Data')
]

file_list = []

for p in paths:
    file_list.extend(p.glob('*.txt'))

# [print(f) for f in file_list]

functors = set()

for f in file_list:
    with open(f) as opened_f:
        for line in opened_f.readlines():
            matches = functor_re.findall(line)
            if matches:
                functors.update(matches)


# [print(f) for f in sorted(functors)]

functor_info = defaultdict(dict)

for f in functors:
    split_res = f.split('(')
    name = split_res[0]
    args = split_res[1].split(')')[0]

    if 'arg_examples' not in functor_info[name]:
        functor_info[name]['arg_examples'] = list()

    functor_info[name]['arg_examples'].append(args)


# [print(item) for item in functor_info.items()]

func_format = '--- Examples:\n{examples}{params}function {func_name}({params_in_func}) end\n\n'

for name in sorted(functor_info.keys()):

    examples = ''
    for arg_example in functor_info[name]['arg_examples']:
        examples += '--- {name}({args})\n'.format(name=name, args=arg_example)

    params = ''
    params_in_func = []
    params_list = sorted(functor_info[name]['arg_examples'], key=lambda x: len(x.split(',')))
    longest_params_list = params_list[-1].split(',')
    for i, p in enumerate(longest_params_list):
        param_type = ''
        p = str(p)

        if p.isdigit():
            param_type = 'number'
        elif p in ('true', 'false'):
            param_type = 'boolean'

        params += f'---@param p{i} {param_type}\n'
        params_in_func.append(f'p{i}')

    print(func_format.format(func_name=name,
                             examples=examples,
                             params=params,
                             params_in_func=', '.join(params_in_func))
          )