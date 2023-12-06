import time

import utils.general_utils as gen_util
import post_process.dawg.DAWG as dw

class SearchDictionary:


    # TODO : The following list should be completed in future
    similar_chars = ['اإأآآِاٌاَاُاِ', 'یبئنپتث', 'جچحخ', 'دذ', 'روزژ', 'سشصض', 'عغ', 'فق', 'کگ', 'طظ']

    def make(self, dict_path):
        """
        reads the dictionary from dict_path and makes the graph needed for search
        :param dict_path: path of dictionary
        :return:
        """
        dawg_obj = dw.DAWG()
        # WordCount = 0
        words = open(dict_path, encoding="utf8").read().split()
        words.sort()
        for word in words:
            # WordCount += 1
            # insert all words, using the reversed version as the data associated with it
            dawg_obj.insert(word, ''.join(reversed(word)))
            # if (WordCount % 100) == 0: print("{0}\r".format(WordCount), end="")
        dawg_obj.finish()
        return dawg_obj

    def check_existence(self, dawg_obj, word):
        """
        check existence of the input word in dictionary using graph object
        :param dawg_obj: dictionary graph
        :param word: word to search
        :return: if exist word in dictionary returns 1, otherwise return 0
        """
        result = dawg_obj.lookup(word)
        if result is None:
            return 0
        return 1


    def save(self, dawg_obj, dawg_file_path):
        """
        saves the graph in pkl format in path specified
        :param dawg_obj: dictionary graph
        :param dawg_file_path: path to save the graph
        :return:
        """
        gen_util.write_array_to_pickle_file(dawg_file_path, dawg_obj)


    def load(self, dawg_file_path):
        """
        loads the graph from the pkl file path specified
        :param dawg_file_path: grah file path
        :return: dictionary graph
        """
        dawg_obj = gen_util.read_array_from_pickle_file(dawg_file_path)
        return dawg_obj

    def index_of_array_elements(self, array, sub_element):
        """
        finds index of element of array contains the sub_element
        For example if the array = ['lor', 'pcg', 'itu', 'dsa'] and sub_element = 'a' then the returned value is 3
        :param array: the input array that the sub_element is searched in it.
        :param sub_element: the sub_element that is searched in array.
        :return: index of sub_element in array.
        """
        index = -1
        for element in array:
            index = index + 1
            if element.__contains__(sub_element):
                return index
        return index

    def find_best_replaced_words(self, dawg_obj, char, word, candidate_chars):
        """
        finds reference words that can be produced by replacing char by candidate_chars in word.
        :param dawg_obj:
        :param char: character that should be replaced in word
        :param word: the word that should be replaced
        :param candidate_chars: the candidate characters that can be replaced by the char
        :param ref_word_list: refernce words list that the replaced words should be checked to be present in it.
        :return: replaced words that are distingushed by | sign
        """
        best_replaced_words = ''
        for candidate_char in candidate_chars:
            if candidate_char != char:
                new_word = word.replace(char, candidate_char)
                if self.check_existence(dawg_obj, word) == 1:
                    best_replaced_words = best_replaced_words + '|' + new_word
        return best_replaced_words.strip('|')

    def find_nearest_words(self, dawg_obj, word):
        """
        finds the best reference word matches the given word based on the similar character replacement and comparision
         with reference words.
        :param dawg_obj:
        :param word: the word that should be replaced by a reference word
        :return: replaced word selected from reference words list in format [main_word|rep_word1|...|rep_wordi]
        """
        replaced_words = '[' + word
        for char in word:
            index = self.index_of_array_elements(self.similar_chars, char)
            if index != -1:
                candidate_chars = self.similar_chars[index]
                best_replaced_words = self.find_best_replaced_words(dawg_obj, char, word, candidate_chars)
                if best_replaced_words != '':
                    replaced_words = replaced_words + '|' + best_replaced_words
        return replaced_words.strip('|') + ']'
