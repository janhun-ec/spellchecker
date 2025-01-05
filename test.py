from spellchecker import SpellChecker
import json

lang = 'en'
text = 'Tihs is a incorect sentence.'
text_zh = '少先队员因该为老人让坐'

# initialize
sp = SpellChecker(lang)

# analyze the text
result = sp.analyze(text, write_to_file=True)
# print(result)
print(json.dumps(result, indent=4, ensure_ascii=False))

# analyze file
file = 'test.txt'
result2 = sp.analyze(file, filemode=True, write_to_file=True, outputfile='results2.json')
print(result2)
# print(json.dumps(result2, indent=4, ensure_ascii=False))
