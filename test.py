from spellchecker import SpellChecker

lang = 'en'
text = 'Tihs is a incorect setnence. Secnod one. I is okay.'

# initialize
sp = SpellChecker(lang)

# analyze the text
result = sp.analyze(text, write_to_file=True)
print(result)

# analyze file
file = 'test.txt'
result2 = sp.analyze(file, filemode=True, write_to_file=True, outputfile='results2.json')
print(result2)
