Tokenization

It can broadly be defined as the process of breaking a string into its constituent parts.

Different types of tokenization:

1) Word level tokenization: 
    Breaking the string into individual words. Eg "I love Chat GPT" would be broken into ['I', 'love', 'Chat, 'GPT']
2) Character level tokenization
    Here we treat each character of the string as the fundamental unit i.e I love Chat GPT would be tokenized to 
    ['I', ' ', 'l', 'o', 'v', 'e', ' ', 'C', 'h', 'a', 't', ' ', 'G', 'P', 'T'] 
3) Sub word tokenization:
    This is in between word level and character level tokenization. Eg the BPE algorithm

The disadvantage of word level tokenization is that it's unable to handle
Out of Vocabulary word(i.e words not seen during training the model) and leads to large vocab sizes

The disadvantage of Character level tokenization is that it leads to longer sequences, which comes with 
increased training and inference time

The Sub word tokenization tries to find a middle ground between these two approaches.

    
BPE

Also called the byte pair encoding algorithm. The algorithm iteratively
replaces the most common pair of characters with a new character until a certain
vocab size is reached 

In this repo I try to replicate the BPE algorithm that is used in the GPT model


Results:

Comparison between tiktoken and my code 



