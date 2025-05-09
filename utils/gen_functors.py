import re
from pathlib import Path

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


[print(f) for f in sorted(functors)]