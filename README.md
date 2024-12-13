# SpellChecker

HunSpell spell checking wrapper, Python module. Checks for mistakes, flags, corrects, and suggests.

### Install
- clone the repo
- run `./get_dicts.sh` to download the dictionaries for hunspell
- dependencies:
    - `pip install -r ./requirements.txt`
    - or run these:
        - `pip install hunspell spacy`
        - `python -m spacy download xx_ent_wiki_sm`  (the spacy multilingual tokenizer package)

### Main method
`SpellChecker.analyze(text, filemode=False, write_to_file=False, outputfile='results.json')`

- returns a `dict` in the form:
```
result = {
    'Corrected': corrected_text,
    'Incorrect words': incorrect_words,
    'Suggestions': suggestions,
}
```

- if `filemode == True` -> `text` contains the filename that will be parsed such as `test.txt`
- if `write_to_file == True` -> the resulting dict will be written to the outputfile in JSON format


### Example usage

```
from spellcheker import SpellChecker

lang = 'hu'
text = 'Hejtelen mondat'

# initialize
sp = SpellChecker(lang)

# analyze the text
result = sp.analyze(text, write_to_file=True)
print(result)

# analyze file
file = 'test.txt'
result2 = sp.analyze(file, filemode=True, write_to_file=True, outputfile='results2.json')
print(result2)
```
First print output:

{
    "Corrected": "Tejtelen mondat",\
    "Incorrect words": [
        "Hejtelen"
    ],\
    "Suggestions": [
        [
            "Tejtelen",
            "Lejtelen",
            "Nejtelen",
            "Pejtelen",
            "Vejtelen",
            "Bejtelen",
            "Fejtelen",
            "Helytelen",
            "Heteljen",
            "Hegtelen"
        ]
    ]
}

### Language Support
Supports the following languages:
| Language      | Code      |
| --------      | -----     |
| Arabic        | (ar)      |
| ~~Chinese~~   | ~~(zh)~~  |
| Czech         | (cs)      |
| English       | (en)      |
| French        | (fr)      |
| German        | (de)      |
| Hungarian     | (hu)      |
| Italian       | (it)      |
| Korean        | (ko)      |
| Polish        | (pl)      |
| Portuguese    | (pt)      |
| Romanian      | (ro)      |
| Russian       | (ru)      |
| Slovakian     | (sk)      |
| Slovenian     | (sl)      |
| Spanish       | (es)      |
| Turkish       | (tr)      |
