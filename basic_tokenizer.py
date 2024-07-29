# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search
# everywhere for classes, files, tool windows, actions, and settings.


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

class BasicTokenizer:

    """
    BPE applies

    """
    def __init__(self):
        self.vocab = {idx: bytes([idx]) for idx in range(256)} ## bytes_int to bytes_string

        self.merges = {} ## (int1, int2) -> idx

    def train(self, text, vocab_size, verbose = False):
        """""
        text: the entire stream of text as unicode code points
        vocab_size: 256 + the number of merges we want to do
        Step1: 
            1) BPE applies merges to byte streams
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
        byte_text = text.encode('utf-8')  # Converts unicode text to byte text

        bytes_list = list(byte_text)  # Converts bytes text to list of integer tokens, range(0,255)

        n_merges = vocab_size - 256

        merge_idx = 256

        for i in range(n_merges):

            pair_count = {}

            ## Code for calcualating max occuring pairs
            for idx in range(len(bytes_list) - 1):

                pair = (bytes_list[idx], bytes_list[idx + 1])

                if pair in pair_count:

                    pair_count[pair] += 1
                else:

                    pair_count[pair] = 1

            merge_candidate = max(pair_count, key = pair_count.get)

            bytes_list = merges(merge_candidate, bytes_list, merge_idx)

            p0, p1 = merge_candidate

            self.vocab[merge_idx] = self.vocab[p0] + self.vocab[p1]

            self.merges[merge_candidate] = merge_idx

            if verbose:
                print(f"merge {i + 1}/{n_merges}: {merge_candidate} -> {merge_idx} ({self.vocab[merge_idx]}) had {pair_count[merge_candidate]} occurrences")

            merge_idx += 1

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
    tokenizer.train(text, 256 + 3, verbose = True)  # 256 are the byte tokens, then do 3 merges
    print(tokenizer.merges)
    print(tokenizer.encode(text))
    encoded = tokenizer.encode(text)
    # [258, 100, 258, 97, 99]
    #print(tokenizer.decode([258, 100, 258, 97, 99]))

    decode = tokenizer.decode(encoded)
    print(decode)

    print(decode == text)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
