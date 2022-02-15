import argparse
import json
from utils import read_words

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
    parser.add_argument('-p', '--pwm', help="output destination of position-weight-matrix")

    args = parser.parse_args()
    words_file = args.words
    pwm_out = args.pwm

    words_list = read_words(words_file)

    pwm = calc_pwm(words_list)

    with open(pwm_out, 'w') as fp:
        json.dump(pwm, fp, indent=4)


if __name__ == '__main__':
    main()