import argparse
import json
from utils import read_words, calc_pwm

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