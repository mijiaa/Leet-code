class TrieNode:
    def __init__(self, char):

        self.char = char
        # list of alphabet size
        # and an inner list to store indexes of the character in current node (this allow O(1) lookup of children node
        self.children = [0] * 26 + [[]]
        self.is_leaf = False  # record if a node is a leaf
        self.is_word = False  # record if a node completes a word
        self.same_prefix_count = 0
        self.prefix_count = 0


class Trie:
    def __init__(self, text):
        """
        Initialise a trie containing the words in the text and generates a Trie object
        :param text: list of strings
        :complexity : O(T) time complexity where T is the total character over all strings in the list
        """
        self.root = TrieNode("")
        self.text = text

        # insert each word to trie
        for i in range(len(text)):
            self.insert(text[i])
        self.saved_node = None
        self.list = []

    def search_prefix(self, prefix):
        """
        search if a prefix exist in Trie
        :param prefix: word to be searched
        :complexity : O(q) time complexity where q is the length of prefix
        :return: True or False
        """
        node = self.root
        for i in range(len(prefix)):
            current_letter = prefix[i]
            current_index = self.to_index(current_letter)
            if node.children[current_index]:
                node = node.children[current_index]
            else:
                return False

        # save last node after a search
        self.saved_node = node
        return True

    def to_index(self, char):
        """
        convert alphabet to numerical representation
        :param char: character to be converted to numerical (0-25)
        :complexity : O(1)
        :return: numerical
        """
        return ord(char) - ord("A") - 32

    def search_full_word(self, word):
        """
        search if a word exist in Trie
        :param word: word to be searched
        :complexity : O(q) time complexity where q is the length of word
        :return: True or False
        """
        node = self.root
        for i in range(len(word)):
            current_letter = word[i]
            current_index = self.to_index(current_letter)
            if node.children[current_index] and node.is_word:
                node = node.children[current_index]
            else:
                return False
        # save last node after a search
        self.saved_node = node
        return True

    def insert(self, text):
        """
        This function insert each text into Trie.
        during insertion :
        1) Duplicates will be ignored, but traversal history through the exact same text will be recorded and increment
        same_prefix_count to calculate string frequency(for function string_feq())
        2) each traversal at node will increment prefix frequency (for function prefix_feq())
        3) method will set a boolean to leaf node to keep track of leaf node ;  last alphabet of a word node to keep track of word

        :param text: word to be inserted
        :complexity :  O(q + search ) time complexity where q is the length of word, search is the complexity for search_full_word() function
        :return:
        """
        node = self.root
        found = self.search_full_word(text)
        if found:  # if word exist, no need to traverse and increment relevant count
            node = self.saved_node
            node.same_prefix_count += 1
        else:
            for i in range(len(text)):
                current_letter = text[i]
                current_index = self.to_index(current_letter)
                if node.children[current_index]:
                    node.is_leaf = False
                    node = node.children[current_index]  # move to child node
                    node.prefix_count += 1  # current node is traversed, increment relevant count

                else:
                    node.is_leaf = False  # new char detected and current node is not a leave anymore
                    new_node = TrieNode(current_letter)
                    node.children[current_index] = new_node
                    node.children[26].append(current_index)  # store indexes at the last pos of children
                    node = node.children[current_index]
                    node.prefix_count += 1  # current node is traversed, increment relevant count

            node.same_prefix_count += 1  # current text forms another prefix so increment relevant count
            node.is_leaf = True  # mark the end of word
            node.is_word = True

    def string_freq(self, query_str):
        """
        this function finds how many times a word occurred in the text.
        :param query_str: is a non-empty string consisting only of lowercase English alphabet characters.
        :complexity : O(q) time complexity where q is the length of query_str
        :return: an integer, which is the number of elements of the text which are exactly query_string
        """
        found = self.search_prefix(query_str)
        # if query is found, go to that node
        if found:
            node = self.saved_node
            # extract relevant count that had been performed during insertion of words and traversal of nodes
            count = node.same_prefix_count
        else:
            return 0
        return count

    def prefix_freq(self, query_str):
        """
        this function finds how many words in the text have that string as a prefix.
        :param query_str: a possibly empty string, with every character in the string being a lowercase English alphabet character.
        :complexity : O(q) time complexity where q is the length of query_str
        :return:
        """
        # if query input is empty, return all strings
        if query_str == '':
            return len(self.text)
        found = self.search_prefix(query_str)
        # if query is found, go to that node
        if found:
            node = self.saved_node
            # extract relevant count that had been performed during insertion of words and traversal of nodes
            count = node.prefix_count
        else:
            return 0
        return count

    def wildcard_prefix_freq(self, query_str):
        """
        this function finds which strings in the text have that string as a prefix, given a string containing a single wildcard
        :param query_str: non-empty string consisting only of lowercase English alphabet characters (possibly no characters),
        and exactly one '?' character, representing a wildcard.
        :return: returns a list containing all the strings which have a prefix which matches query_str, in lexicographic order.
        :complexity: O(q + S) where q is the length of query_str, where S is the total number of characters in all strings
        of the text (inclusive of duplicates) which have a prefix matching query_str.
        """
        query_str = query_str.split('?')  # remove wildcard by splitting
        node = self.root
        result = []

        # if wildcard is at the last of query (exp : "a?")
        if query_str[1] == '':
            #if query is found, go to that node
            if self.search_prefix(query_str[0]):
                node = self.saved_node

            # get the alphabets of children nodes using stored indexes in node.children[26]
            # and concatenate them with query to form a proper prefix
            # then this prefix is used in traversing (traverse())to find words

            index = node.children[26]
            index = counting_sort(index)  # counting sort index so that alphabets will be in lexicographic order.
            temp_string = [""] * len(index)
            for i in range(len(index)):
                temp_string[i] = query_str[0] + node.children[index[i]].char
            for i in range(len(temp_string)):
                if self.search_prefix(temp_string[i]):
                    node = self.saved_node
                    self.traverse(node, temp_string[i], result)

        # if wildcard before the query (exp : "?a")
        elif query_str[0] == '':
            index = node.children[26]
            index = counting_sort(index)
            temp_string = [""] * len(index)
            for i in range(len(index)):
                temp_string[i] = node.children[index[i]].char + query_str[1]
            for i in range(len(temp_string)):
                if self.search_prefix(temp_string[i]):
                    node = self.saved_node
                    self.traverse(node, temp_string[i], result)

        # if wildcard is at the middle of the query (exp : "a?a")
        else:
            if self.search_prefix(query_str[0]):
                node = self.saved_node
            index = node.children[26]
            index = counting_sort(index)
            temp_string = [""] * len(index)
            for i in range(len(index)):
                temp_string[i] = query_str[0] + node.children[index[i]].char + query_str[1]
            for i in range(len(temp_string)):
                if self.search_prefix(temp_string[i]):
                    node = self.saved_node
                    self.traverse(node, temp_string[i], result)
        return result

    def traverse(self, node, query_str, result):
        """
        traverse the trie and find and form words
        :param node: current node
        :param query_str: non-empty string consisting only of lowercase English alphabet characters
        :param result: list of strings
        :complexity: O(q + S) where q is the length of query_str, where S is the total number of characters in all strings
        of the text (inclusive of duplicates) which have a prefix matching query_str.
        """

        # if leaf node is reached, means a word is formed, append current query string
        if node.is_leaf:
            # append all duplicates of current word
            count = self.string_freq(query_str)
            for i in range(count):
                result.append(query_str)
        # node is not a leaf node but this node forms a word, append current string
        elif node.is_word:
            count = self.string_freq(query_str)
            for i in range(count):
                result.append(query_str)

        index = counting_sort(node.children[26])
        # recurse to children node
        for i in range(len(index)):
            char = node.children[index[i]].char
            query_str += char
            self.traverse(node.children[index[i]], query_str, result)
            query_str = query_str[:-1]


def counting_sort(num_lst):
    """
    sort stored indexes in trie, modified from my assignment 1
    :param num_lst: list of positive integers
    :complexity : O(N) where N is the length of input list
    :return: sorted list
    """
    n = len(num_lst)
    # initialise counter list with base
    counter = [0 for i in range(26)]
    # for each value in input list, store count of each element at their respective indexes
    for element in num_lst:
        counter[element] += 1

    # calculate the cumulative sum
    for j in range(1,len(counter)):
        counter[j] += counter[j-1]

    result = [ 0 for i in range(n)]

    # construct output
    for k in range(n-1,-1,-1):
        # calculate key to point to position in counter list
        # set output[position[key] - 1] to the val from input
        key = num_lst[k]
        result[counter[key] -1] = num_lst[k]
        # decrement counter
        counter[key] -=1

    for i in range(n):
        num_lst[i] = result[i]
    return num_lst






