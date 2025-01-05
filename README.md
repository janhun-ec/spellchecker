# SpellChecker

Spell checking wrapper, Python module. Checks for mistakes, flags, corrects, and suggests. Uses mostly LanguageTool, then HunSpell, pycorrector, depending on the language.

### Install
- clone the repo
- run `./get_dicts.sh` to download the dictionaries for hunspell
- dependencies:
    - `pip install -r ./requirements.txt`
    - or run these:
        - `pip install hunspell spacy language_tool_python pycorrector torch kenlm`
        - `python -m spacy download xx_ent_wiki_sm`  (the spacy multilingual tokenizer package)

### Main method
`SpellChecker.analyze(text, filemode=False, write_to_file=False, outputfile='results.json')`

- returns a `dict` in the form:
```
result = {
    "OriginalText": text,
    "Errors": [
        {
            "Word": incorrect_word,
            "StartPosition": position,
            "ErrorType": error_type,
            "Suggestions": [
                suggestion1,
                suggestion2,
                ...
            ],
            "SpellCheckerTool": tool_name
        },
        ...
    ]
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
```
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
```

### Language Support
Supports the following languages:
| Language      | Code      | Tool          |
| --------      | -----     | ----          |
| Arabic        | (ar)      | LanguageTool  |
| Chinese       | (zh)      | pycorrector   |
| Czech         | (cs)      | HunSpell      |
| English       | (en)      | LanguageTool  |
| French        | (fr)      | LanguageTool  |
| German        | (de)      | LanguageTool  |
| Hungarian     | (hu)      | HunSpell      |
| Italian       | (it)      | LanguageTool  |
| Korean        | (ko)      | HunSpell      |
| Polish        | (pl)      | LanguageTool  |
| Portuguese    | (pt)      | LanguageTool  |
| Romanian      | (ro)      | HunSpell      |
| Russian       | (ru)      | LanguageTool  |
| Slovakian     | (sk)      | HunSpell      |
| Slovenian     | (sl)      | LanguageTool  |
| Spanish       | (es)      | HunSpell      |
| Turkish       | (tr)      | HunSpell      |
