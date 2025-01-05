# SpellChecker

Spell checking wrapper, Python module. Checks for mistakes, flags, corrects, and suggests. Uses mostly LanguageTool, then HunSpell, pycorrector, hanspell, depending on the language.

### Install
- clone the repo
- run `./get_dicts.sh` to download the dictionaries for hunspell
- dependencies:
    - `pip install -r ./requirements.txt`
    - or run these:
        - `pip install hunspell spacy language_tool_python`
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

lang = 'en'
text = 'Tihs is a incorect sentence.'

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
    "OriginalText": "Tihs is a incorect sentence.",
    "Errors": [
        {
            "Word": "Tihs",
            "StartPosition": 0,
            "ErrorType": "misspelling morfologik rule en us",
            "Suggestions": [
                "This",
                "Ties",
                "Tips",
                "IHS",
                "Tics",
                "TCHS",
                "THS",
                "TIS",
                "Tins",
                "Tits"
            ],
            "SpellCheckerTool": "languagetool"
        },
        {
            "Word": "a",
            "StartPosition": 8,
            "ErrorType": "misspelling en a vs an",
            "Suggestions": [
                "an"
            ],
            "SpellCheckerTool": "languagetool"
        },
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
