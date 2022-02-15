import argparse
import json
from utils import read_words

def char_freq(words):
    freq = {}

    # use ASCII values to add keys to dict for each lower case letter
    for i in range(97, 123):
        char = chr(i)
        freq[char] = 0.0

    # count the total number of characters and number of times each letter appears
    total_chars = 0
    for word in words:
        for char in word:
            freq[char] += 1
            total_chars += 1
    for char in freq:
        freq[char] = freq[char] / total_chars

    return freq


def calc_pwm(words):
    # initialize position-weight-matrix with keys as position and value as a dictionary containing freq of each letter
    pwm = {}
    for i in range(5):
        pwm[i] = {}
        for j in range(97, 123):
            pwm[i][chr(j)] = 0.0


    for word in words:
        for pos, char in enumerate(word):
            pwm[pos][char] += 1
    
    total_words = len(words)
    for pos in pwm:
        for char in pwm[pos]:
            pwm[pos][char] = pwm[pos][char] / total_words
    
    return pwm



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--words', help="input file containing words to be analyzed")
    parser.add_argument('-c', '--chars', help="output destination of character frequencies")
    parser.add_argument('-p', '--pwm', help="output destination of position-weight-matrix")

    args = parser.parse_args()
    words_file = args.words
    char_out = args.chars
    pwm_out = args.pwm

    words_list = read_words(words_file)

    freq = char_freq(words_list)
    pwm = calc_pwm(words_list)
    
    with open(char_out, 'w') as fp:
        json.dump(freq, fp, indent=4)

    with open(pwm_out, 'w') as fp:
        json.dump(pwm, fp, indent=4)


if __name__ == '__main__':
    main()