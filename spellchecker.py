"""Module for spellchecking a text."""

from json import dump
import sys
from spacy import load
from hunspell import HunSpell, HunSpellError
from language_tool_python import LanguageTool
from pycorrector import Corrector


class SpellChecker:
    """Class for analyzing and correcting text in languages"""

    def __init__(self, lang='en', dicts_path='./dicts'):
        self.lang = lang
        self.dicts_path = dicts_path
        self.nlp = self.__get_tokenizer()

        self.languagetool_lang_codes = {
                'ar': 'ar',
                'de': 'de-DE',
                'en': 'en-US',
                'es': 'es',
                'fr': 'fr',
                'it': 'it',
                'pl': 'pl-PL',
                'pt': 'pt',
                # 'ro': 'ro-RO',    # hunspell is better for this
                'ru': 'ru-RU',
                # 'sk': 'sk-SK',    # hunspell is better for this
                'sl': 'sl-SI',
                # 'zh': 'zh-CN',    # pycorrector
            }

        self.spellchecker = self.__get_corrector()


    def __get_tool(self):
        """decides which spell checking tool to use. Hunspell or Languagetool..."""
        if self.lang in self.languagetool_lang_codes:
            return 'languagetool'
        if self.lang in ['zh']:
            return 'pycorrector'
        return 'hunspell'


    def __get_corrector(self):
        """Returns spellchecker object for the specific language"""
        self.tool = self.__get_tool()

        if self.tool == 'hunspell':
            try:
                return HunSpell(f'{self.dicts_path}/{self.lang}.dic',\
                                 f'{self.dicts_path}/{self.lang}.aff')
            except HunSpellError:
                sys.exit('Dictionaries missing, run ./get_dicts.sh to download them.')

        if self.tool == 'languagetool':
            lang_code = self.languagetool_lang_codes[self.lang]
            return LanguageTool(lang_code)

        if self.tool == 'pycorrector':
            return Corrector()


    def __get_tokenizer(self):
        """loads spacy package for tokenizing"""
        multilang = 'xx_ent_wiki_sm'
        # nlp_dataset = {
        #     'en': 'en_core_web_sm',
        #     'hu': 'hu_core_news_md',
        #     'ro': 'ro_core_news_sm',
        #     'zh': 'zh_core_web_sm',
        #     'fr': 'fr_core_news_sm',
        #     'de': 'de_core_news_sm',
        #     'it': 'it_core_news_sm',
        #     'ko': 'ko_core_news_sm',
        #     'pl': 'pl_core_news_sm',
        #     'pt': 'pt_core_news_sm',
        #     'ru': 'ru_core_news_sm',
        #     'sl': 'sl_core_news_sm',
        #     'es': 'es_core_news_sm',
        #     'ar': multilang,
        #     'cs': multilang,
        #     'sk': multilang,
        #     'tr': multilang,
        # }

        nlp = load(multilang)  # nlp_dataset[self.lang]
        nlp.add_pipe('sentencizer')
        return nlp


    def __tokenize(self, string):
        """Tokenizes string with spacy package"""
        doc = self.nlp(string)
        tokenized = [str(token) for token in doc]
        return tokenized


    def __hunspell_corrector(self, text):
        """corrects text with hunspell spell checker.
        splits text by spaces"""
        corrected = ''
        incorrect_words = []
        suggestions = []
        positions = []

        sent_position = 0
        for word in text.split(' '):    # splitting by space
            tokenized = self.__tokenize(word)   # further splitting into tokens (e.g.: i'm -> i 'm)

            word_position = 0
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

                    positions.append(sent_position + word_position)

                word_position += len(token)

            corrected += ' '
            sent_position += len(word) + 1   # plus 1 for the space

        corrected = corrected[:-1]  # remove last added space

        error_types = ['Misspelling'] * len(incorrect_words)

        return corrected, incorrect_words, suggestions, positions, error_types


    def __languagetool_corrector(self, text):
        """corrects and analyses text with languagetool"""
        incorrect_words = []
        suggestions = []
        positions = []
        error_types = []
        corrected = []

        matches = self.spellchecker.check(text)
        for match in matches:
            offset = match.offset
            positions.append(offset)

            incorrect_word = text[offset: offset + match.errorLength]
            incorrect_words.append(incorrect_word)

            suggestions.append(match.replacements)

            # ruleId or ruleIssueType or category or message? or combined?
            error_types.append(match.ruleIssueType + ' ' + match.ruleId.replace('_', ' ').lower())

        # if correction needed too
        # corrected.append(self.spellchecker.correct(text))

        return corrected, incorrect_words, suggestions, positions, error_types


    def __pycorrector_corrector(self, text):
        """corrects and analyses text with pycorrector"""
        incorrect_words = []
        suggestions = []
        positions = []
        error_types = []
        corrected = []

        result = self.spellchecker.correct(text)
        for error in result['errors']:
            incorrect_word = error[0]
            corretction = error[1]
            position = error[2]

            incorrect_words.append(incorrect_word)
            suggestions.append(corretction)
            positions.append(position)

            error_types.append('Misspelled')

        corrected.append(result['target'])

        return corrected, incorrect_words, suggestions, positions, error_types


    def analyze(self, text, filemode=False, write_to_file=False, outputfile='results.json'):
        """Parses the text, builds structured response with errors"""
        if filemode:
            with open(text, 'r', encoding="utf-8") as f:
                text = f.read()

        if self.tool == 'languagetool':
            corrected, incorrect_words, suggestions, positions, error_types = \
                self.__languagetool_corrector(text)
        elif self.tool == 'pycorrector':
            corrected, incorrect_words, suggestions, positions, error_types = \
                self.__pycorrector_corrector(text)
        elif self.tool == 'hunspell':
            corrected, incorrect_words, suggestions, positions, error_types = \
                self.__hunspell_corrector(text)
        else:
            sys.exit('No tool for this language')

        errors = []
        for i, incorrect_word in enumerate(incorrect_words):
            curr_suggestions = suggestions[i]
            position = positions[i]
            error_type = error_types[i]

            error = {
                'Word': incorrect_word,
                'StartPosition': position,
                'ErrorType': error_type,
                'Suggestions': curr_suggestions,
                'SpellCheckerTool': self.tool,
            }
            errors.append(error)

        result = {
            'OriginalText': text,
            'Errors': errors,
        }

        if write_to_file:
            self.__write(outputfile, result)

        return result


    def __write(self, filename, result):
        """Writes the resulting json to file"""
        with open(filename, 'w', encoding="utf-8") as g:
            dump(result, g, indent=4, ensure_ascii=False)
