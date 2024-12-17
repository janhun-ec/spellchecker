from json import dump
from hunspell import HunSpell
from language_tool_python import LanguageTool
from spacy import load


class SpellChecker:
    """Class for analyzing and correcting text in languages"""

    def __init__(self, lang='en', dicts_path='./dicts'):
        self.lang = lang
        self.dicts_path = dicts_path
        self.nlp = load('xx_ent_wiki_sm')
        self.not_supported_langs = ['zh']
        self.spellchecker = self.__get_obj(lang)


    def __get_tool(self, lang):
        if lang in ['en', 'fr', 'pl', 'de', 'pt','es']:
            return 'languagetool'
        elif lang in ['zh']:
            # TODO get chinese spellchecker
            return 'hunspell'
        else:
            return 'hunspell'


    def __get_obj(self, lang):
        """Returns Hunspell spellchecker for the specific language"""
        if lang in self.not_supported_langs:
            lang = 'en'
        self.tool = self.__get_tool(lang)
        if self.tool == 'hunspell':
            try:
                return HunSpell(f'{self.dicts_path}/{lang}.dic', f'{self.dicts_path}/{lang}.aff')
            except:
                print('Dictionaries missing, run ./get_dicts.sh to download them.')
                quit()
        elif self.tool == 'languagetool':
            return LanguageTool(lang)


    def __tokenize(self, string):
        """Tokenizes string with spacy package"""
        doc = self.nlp(string)
        tokenized = [str(token) for token in doc]
        return tokenized


    def __correct_chunk(self, chunk):
        """
        Text is separated by spaces into chunks.
        Actual spellchecking and correction.
        """
        tokenized = self.__tokenize(chunk)
        # doc = self.nlp(chunk)
        incorrect_words = []
        suggestions = []
        corrected = ''
        for token in tokenized:
            if not token.isalpha():     # if not word
                corrected += token
            elif self.spellchecker.spell(token):    # word found in dict
                corrected += token
            else:   # not found
                incorrect_words.append(token)

                curr_suggestions = self.spellchecker.suggest(token)
                suggestions.append(curr_suggestions)

                corrected += curr_suggestions[0] if curr_suggestions else token

        return corrected, incorrect_words, suggestions


    def __hunspell_corrector(self, text):
        corrected = ''
        incorrect_words = []
        suggestions = []

        for token in text.split(' '):
            curr_corrected, curr_incorrect_words, curr_suggestions = self.__correct_chunk(token)
            corrected += curr_corrected + ' '
            incorrect_words.extend(curr_incorrect_words)
            suggestions.extend(curr_suggestions)

        corrected = corrected[:-1]
        
        return corrected, incorrect_words, suggestions


    def __languagetool_corrector(self, text):
        # TODO
        return self.__hunspell_corrector(text)


    def analyze(self, text, filemode=False, write_to_file=False, outputfile='results.json'):
        """Parses the text, splits by spaces, builds the corrected sentence"""
        if filemode:
            with open(text, 'r', encoding="utf-8") as f:
                text = f.read()

        if self.tool == 'hunspell':
            corrected, incorrect_words, suggestions = self.__hunspell_corrector(text)
        elif self.tool == 'languagetool':
            corrected, incorrect_words, suggestions = self.__languagetool_corrector(text)

        result = {
            'Corrected': corrected,
            'Incorrect words': incorrect_words,
            'Suggestions': suggestions,
            }

        if write_to_file:
            self.__write(outputfile, result)

        return result


    def __write(self, filename, result):
        """Writes the resulting json to file"""
        with open(filename, 'w', encoding="utf-8") as g:
            dump(result, g, indent=4, ensure_ascii=False)
