import os
import re
from q2 import boyer_moore
# from knuth_morris_pratt import kmp

"""
    Expected return is an list with '0' indexing and the first index of the pattern recognised
"""


#Retrieve Patterns
script_dir = os.path.dirname(__file__)


patterns = []
pat_path = os.path.join(script_dir, "Tests", "BoyerMoore_Pat.txt")

with open(pat_path, mode="r", encoding="utf-8-sig") as f:
    for line in f:
        if len(line) > 0:
            if line[0] != '#':
                patterns.append(line.strip())

#Retrieve texts
texts = []
text_path = os.path.join(script_dir, "Tests", "BoyerMoore_Text.txt")
with open(text_path, mode="r", encoding="utf-8-sig") as f:
    for line in f:
        if len(line) > 0:
            if line[0] != '#':
                texts.append(line.strip())

for pat in patterns:
    for text in texts:
        bm_result = boyer_moore(text, pat)
        # bm_result = kmp(text, pat)
        re_result = []
        for match in re.finditer(f'(?=({pat}))', text, flags=re.IGNORECASE):
            re_result.append(match.start())
        if (bm_result != re_result):
            print(f'    bm_result = {bm_result} \n    re_result={re_result}')
            print(f'text = {text}')
            print(f'pat = {pat}')

        #Use regex as the expected behaviour

