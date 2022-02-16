import json, argparse, sys, time
from selenium import webdriver
from pyshadow.main import Shadow
from pathlib import Path
import os.path as osp
from datetime import date
from ny_times_connector import NYTimesConnector

parentdir = Path(__file__).parents[1]
sys.path.append(osp.join(parentdir, 'scripts'))

from utils import get_best_word, read_words, tweet_score


def play_wordle(words_list, pwm, connector):
    connector.start()
    time.sleep(1)
    connector.close_instructions()
    # use ASCII to generate list of all lower-case letters
    # all letters are possible in each pos (to start)
    letters_by_pos = {
        0: [chr(i) for i in range(97, 123)],
        1: [chr(i) for i in range(97, 123)],
        2: [chr(i) for i in range(97, 123)],
        3: [chr(i) for i in range(97, 123)],
        4: [chr(i) for i in range(97, 123)]
    }

    # tracking yellow tiles
    present_letters = []

    # guess words until solved or out of guesses
    solved = False 
    attempt = 0
    score_board = ''
    while not solved and attempt < 6:
        attempt += 1
        word = get_best_word(words_list, letters_by_pos, present_letters)['word']
        response = connector.submit_guess(word)

        solved = True
        score_row = ''
        for pos, (letter, eval) in enumerate(response):
            if eval == 'present':
                solved = False
                score_row += '🟨'
                # remove the letter from this pos (since not correct)
                if letter in letters_by_pos[pos]: letters_by_pos[pos].remove(letter)

                # send a flag signalling this letter MUST be in the word
                present_letters.append(letter)
            
            elif eval == 'correct':
                score_row += '🟩'
                # this position can only be the letter
                letters_by_pos[pos] = [letter]

            # eval == absent
            else:
                solved = False
                score_row += '⬛️'
                # remove the letter from each pos
                for pos in letters_by_pos:
                    if letters_by_pos[pos] == [letter]: continue
                    elif letter in letters_by_pos[pos]: letters_by_pos[pos].remove(letter)

        if not solved:
            score_row += '\n'

        score_board += (score_row)
        time.sleep(3)

    if solved:
        print(f"Wordle-bot solved today's wordle in {attempt} tries!")
    else:
        print("Wordle-bot couldn't solve today's wordle :(")
        attempt = 'X'
    
    score_header = connector.score_header(attempt)
    # Close the tab when finished
    connector.exit()


    score_board = score_header + score_board
    return score_board


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--words')
    parser.add_argument('-p', '--pwm')
    parser.add_argument('-t', '--tweet', default=False, type=bool)

    args = parser.parse_args()
    words_file = args.words
    pwm_file = args.pwm
    tweet = args.tweet

    words_list = read_words(words_file)

    # NOTE: json.load() automatically converts keys into strings, thus they are no longer ints!
    pwm = json.load(open(pwm_file, 'r'))
    ny_times_connector = NYTimesConnector()

    score_board = play_wordle(words_list, pwm, ny_times_connector)
    print(score_board)
    if tweet:
        tweet_score(score_board)

if __name__ == '__main__':
    main()