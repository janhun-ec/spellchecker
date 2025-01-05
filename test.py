from spellchecker import SpellChecker

lang = 'zh'
text = '少先队员因该为老人让坐'

# initialize
sp = SpellChecker(lang)

# analyze the text
result = sp.analyze(text, write_to_file=True)
print(result)

# analyze file
# file = 'test.txt'
# result2 = sp.analyze(file, filemode=True, write_to_file=True, outputfile='results2.json')
# print(result2)
