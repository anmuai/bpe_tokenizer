# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.\

import regex as re

def merges(merge_candidate, bytes_list, merge_idx):

    bytes_tokens_copy = []
    idx = 0
    while idx < len(bytes_list) - 1:
        pair = (bytes_list[idx], bytes_list[idx + 1])
        if pair == merge_candidate:
            bytes_tokens_copy.append(merge_idx)
            idx += 2
        else:
            bytes_tokens_copy.append(bytes_list[idx])
            idx += 1
    if idx == len(bytes_list) - 1:
        bytes_tokens_copy.append(bytes_list[idx])
    bytes_list = bytes_tokens_copy

    return bytes_list
class RegexTokenizer:
    """
    BPE applies

    """

    def __init__(self):
        self.vocab = {idx: bytes([idx]) for idx in range(256)}  ## bytes_int to bytes_string

        self.gpt4_split  = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""

        self.merges = {}  ## (int1, int2) -> idx

    def train(self, text, vocab_size, verbose=False):
        """""
        text: the entire stream of text as unicode code points
        vocab_size: 256 + the number of merges we want to do
        Step1: 
            1) BPE applies merges to byte streams
            2) Split the text to chunks based on split pattern
            2) Convert the unicode string to byte streams utf-8
        Step2:
            1) Perform merges
                merge logic:
                    1) find the most common consecutive list of ints
                    2) store that in the merges dictionary
                    3) Increment the merges idx and repeat until desired merges obtained
            2) Once merges dictionary is created 
            3) create a vocab dictionary where 0 to 255 will be bytes representations
            4) Beyond 255 perform incorporate the merges(by merging the byte indices)

        """""

        pattern = re.compile(self.gpt4_split)

        words = re.findall(pattern, text)

        bytes_words = [word.encode('utf-8') for word in words]  # Converts unicode text to byte text

        bytes_words = [list(char) for char in bytes_words]  # Converts bytes text to list of integer tokens, range(0,255)

        n_merges = vocab_size - 256

        merge_idx = 256

        for _ in range(n_merges):
            pair_count = {}
            ## Create a dictionary with pairs and their oocurrence in training data
            for token in bytes_words:
                for idx in range(len(token) - 1): ## Loop gets excuted token has atleast two elements
                    pair = (token[idx], token[idx + 1])
                    if pair in pair_count:
                        pair_count[pair] += 1
                    else:
                        pair_count[pair] = 1

            if len(pair_count) == 0:
                break

            ## Find the pair to be merged
            merge_candidate = max(pair_count, key = pair_count.get)

            for idx in range(len(bytes_words)):
                token = merges(merge_candidate, bytes_words[idx], merge_idx)
                bytes_words[idx] = token

            self.merges[merge_candidate] = merge_idx

            merge_idx += 1

        for (p0, p1), idx in self.merges.items():
            self.vocab[idx] = self.vocab[p0] + self.vocab[p1]  # concatenating two byte strings
        # if verbose:
        #     for idx, bstring in self.vocab.items():
        #         print(f"token number {idx} is ")

    def encode(self, text):
        """
        Encode means converting a stream of unicode text to list
        of byte ints
        :param text:
        :return:
        """
        bytes_text = text.encode('utf-8')

        bytes_list = list(bytes_text)  # Converts bytes string to list of base 10 ints

        for (p0, p1), merge_idx in self.merges.items():
            bytes_list = merges((p0, p1), bytes_list, merge_idx)

        return bytes_list

    def decode(self, ids):
        """

        decode means converting list of ints to strings


        :param ids:
        :return:
        """
        string = b''
        for id in ids:
            string += self.vocab[id]
        return string.decode('utf-8')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tokenizer = BasicTokenizer()
    text = "aaabdaaabac"
    tokenizer.train(text, 256 + 3)  # 256 are the byte tokens, then do 3 merges
    print(tokenizer.encode(text))
    # [258, 100, 258, 97, 99]
    print(tokenizer.decode([258, 100, 258, 97, 99]))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
