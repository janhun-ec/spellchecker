from json import dump
from hunspell import HunSpell
from spacy import load


class SpellChecker:
    """Class for analyzing and correcting text in languages"""

    def __init__(self, lang='en', dicts_path='./dicts'):
        self.lang = lang
        self.dicts_path = dicts_path
        self.nlp = load('xx_ent_wiki_sm')
        self.not_supported_langs = ['zh']
        self.spellchecker = self.__get_obj(lang)


    def __get_obj(self, lang):
        """Returns Hunspell spellchecker for the specific language"""
        if lang in self.not_supported_langs:
            lang = 'en'
        try:
            return HunSpell(f'{self.dicts_path}/{lang}.dic', f'{self.dicts_path}/{lang}.aff')
        except:
            print('Dictionaries missing, run ./get_dicts.sh to download them.')
            quit()


    def __tokenize(self, string):
        """Tokenizes string with spacy package"""
        doc = self.nlp(string)
        tokenized = [str(token) for token in doc]
        return tokenized


    def __correct_chunk(self, chunk, position):
        """
        Text is separated by spaces into chunks.
        Actual spellchecking and correction.
        """
        tokenized = self.__tokenize(chunk)
        incorrect_words = []
        suggestions = []
        corrected = ''
        positions = []

        curr_position = 0
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

                positions.append(position + curr_position)
            
            curr_position += len(token)

        return corrected, incorrect_words, suggestions, positions


    def analyze(self, text, filemode=False, write_to_file=False, outputfile='results.json'):
        """Parses the text, splits by spaces, builds the corrected sentence"""
        if filemode:
            with open(text, 'r', encoding="utf-8") as f:
                text = f.read()

        corrected = ''
        incorrect_words = []
        suggestions = []
        positions = []

        position = 0
        for token in text.split(' '):
            curr_corrected, curr_incorrect_words, curr_suggestions, curr_positions = self.__correct_chunk(token)
            corrected += curr_corrected + ' '
            incorrect_words.extend(curr_incorrect_words)
            suggestions.extend(curr_suggestions)
            positions.extend(curr_positions)
            position += len(token) + 1

        corrected = corrected[:-1]


        # build up the errors
        error_type = 'Misspelling'
        tool = 'HunSpell'
        errors = []

        for i, incorrect_word in enumerate(incorrect_words):
            curr_suggestions = suggestions[i]
            position = positions[i]

            error = {
                'Word': incorrect_word,
                'StartPosition': position,
                'ErrorType': error_type,
                'Suggestions': curr_suggestions,
                'SpellCheckerTool': tool,
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
