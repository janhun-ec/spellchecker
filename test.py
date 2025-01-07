from spellchecker import SpellChecker
import json

lang = 'en'
text = 'Tihs is a incorect sentence.'

# initialize
sp = SpellChecker(lang)

# analyze the text
result = sp.analyze(text, write_to_file=True)
# print(result)
print(json.dumps(result, indent=4, ensure_ascii=False))

# analyze file
name = f'example_{lang}2'
file = f'examples/{name}.txt'
result2 = sp.analyze(file, filemode=True, write_to_file=True, outputfile=f'examples/{name}.json')
print(result2)
# print(json.dumps(result2, indent=4, ensure_ascii=False))
