from json import dump
from hunspell import HunSpell
from language_tool_python import LanguageTool
from spacy import load


class SpellChecker:
    """Class for analyzing and correcting text in languages"""

    def __init__(self, lang='en', dicts_path='./dicts'):
        self.lang = lang
        self.dicts_path = dicts_path
        self.nlp = self.__get_tokenizer()
        self.spellchecker = self.__get_corrector()


    def __get_tool(self):
        """decides which spell checking tool to use. Hunspell or Languagetool..."""
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
                'zh': 'zh-CN',
            }

        if self.lang in self.languagetool_lang_codes:
            return 'languagetool'
        elif self.lang in ['zh']:
            # TODO get chinese spellchecker. pycorrector
            return 'languagetool'
        elif self.lang in ['ko']:
            # TODO hanspell?
            return 'hunspell'
        else:
            return 'hunspell'


    def __get_corrector(self):
        """Returns spellchecker object for the specific language"""
        self.tool = self.__get_tool()
        
        if self.tool == 'hunspell':
            try:
                return HunSpell(f'{self.dicts_path}/{self.lang}.dic', f'{self.dicts_path}/{self.lang}.aff')
            except:
                print('Dictionaries missing, run ./get_dicts.sh to download them.')
                quit()
        elif self.tool == 'languagetool':
            lang_code = self.languagetool_lang_codes[self.lang]
            return LanguageTool(lang_code)


    def __get_tokenizer(self):
        """loads spacy package for tokenizing"""
        multilang = 'xx_ent_wiki_sm'
        nlp_dataset = {
            'en': 'en_core_web_sm',
            'hu': 'hu_core_news_md',
            'ro': 'ro_core_news_sm',
            'zh': 'zh_core_web_sm',
            'fr': 'fr_core_news_sm',
            'de': 'de_core_news_sm',
            'it': 'it_core_news_sm',
            'ko': 'ko_core_news_sm',
            'pl': 'pl_core_news_sm',
            'pt': 'pt_core_news_sm',
            'ru': 'ru_core_news_sm',
            'sl': 'sl_core_news_sm',
            'es': 'es_core_news_sm',
            'ar': multilang,
            'cs': multilang,
            'sk': multilang,
            'tr': multilang,
        }

        return load(nlp_dataset[self.lang])


    def __tokenize(self, string):
        """Tokenizes string with spacy package"""
        doc = self.nlp(string)
        tokenized = [str(token) for token in doc]
        return tokenized


    def __correct_chunk(self, chunk):
        """
        Text is separated by spaces into chunks.
        Actual hunspell spellchecking and correction.
        """
        tokenized = self.__tokenize(chunk)
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
        """corrects text with hunspell spell checker.
        splits text by spaces"""
        corrected = ''
        incorrect_words = []
        suggestions = []

        for token in text.split(' '):
            curr_corrected, curr_incorrect_words, curr_suggestions = self.__correct_chunk(token)
            corrected += curr_corrected + ' '
            incorrect_words.extend(curr_incorrect_words)
            suggestions.extend(curr_suggestions)

        corrected = corrected[:-1]  # remove last added space

        positions, error_types = None, None

        return corrected, incorrect_words, suggestions, positions, error_types


    def __languagetool_corrector(self, text):
        """corrects and analyses text with languagetool"""
        incorrect_words = []
        suggestions = []
        positions = []
        error_types = []
        corrected = []

        # split by sentence
        doc = self.nlp(text)
        sents = [str(sent) for sent in doc.sents]
        for sent in sents:
            matches = self.spellchecker.check(sent)
            for match in matches:
                offset = match.offset
                positions.append(offset + text.find(sent))

                incorrect_word = sent[offset: offset + match.errorLength]
                incorrect_words.append(incorrect_word)

                suggestions.append(match.replacements)

                # TODO ruleId or ruleIssueType or category or message? or combined?
                error_types.append(match.ruleIssueType + ' ' + match.ruleId)

            corrected.append(self.spellchecker.correct(sent))

        return corrected, incorrect_words, suggestions, positions, error_types


    def analyze(self, text, filemode=False, write_to_file=False, outputfile='results.json'):
        """Parses the text, builds structured response with errors"""
        if filemode:
            with open(text, 'r', encoding="utf-8") as f:
                text = f.read()

        if self.tool == 'hunspell':
            corrected, incorrect_words, suggestions, positions, error_types = self.__hunspell_corrector(text)
        elif self.tool == 'languagetool':
            corrected, incorrect_words, suggestions, positions, error_types = self.__languagetool_corrector(text)

        result = {
            'Corrected': corrected,
            'Incorrect words': incorrect_words,
            'Suggestions': suggestions,
            'Positions': positions,
            'Error Types': error_types,
            }

        if write_to_file:
            self.__write(outputfile, result)

        return result


    def __write(self, filename, result):
        """Writes the resulting json to file"""
        with open(filename, 'w', encoding="utf-8") as g:
            dump(result, g, indent=4, ensure_ascii=False)
