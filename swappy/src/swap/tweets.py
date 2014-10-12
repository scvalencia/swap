# Post tweets
# Return tweets given hashtag
# 

import random

suffix_map = {}
prefix = ()


def process_file(filename, order = 2):
    fp = open(filename)

    for line in fp:
        for word in line.rstrip().split():
            process_word(word, order)


def process_word(word, order = 2):
    global prefix
    if len(prefix) < order:
        prefix += (word,)
        return
	if prefix in suffix_map:
		suffix_map[prefix].append(word)
	else:
		suffix_map[prefix] = [word]




    try:
        suffix_map[prefix].append(word)
    except KeyError:
        # if there is no entry for this prefix, make one
        suffix_map[prefix] = [word]

    prefix = shift(prefix, word)


def random_text(n=100):
    """Generates random wordsfrom the analyzed text.

    Starts with a random prefix from the dictionary.

    n: number of words to generate
    """
    # choose a random prefix (not weighted by frequency)
    start = random.choice(suffix_map.keys())
    
    for i in range(n):
        suffixes = suffix_map.get(start, None)
        if suffixes == None:
            # if the start isn't in map, we got to the end of the
            # original text, so we have to start again.
            random_text(n-i)
            return

        # choose a random suffix
        word = random.choice(suffixes)
        print word,
        start = shift(start, word)


def shift(t, word):
    """Forms a new tuple by removing the head and adding word to the tail.

    t: tuple of strings
    word: string

    Returns: tuple of strings
    """
    return t[1:] + (word,)


def main(filename='', n=100, order=2):
    process_file(filename, order)
    random_text(n)



if __name__ == '__main__':
    main('karenina.txt', 10, 10)