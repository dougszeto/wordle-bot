import json, argparse, sys, time
from selenium import webdriver
from pyshadow.main import Shadow
from pathlib import Path
import os.path as osp

parentdir = Path(__file__).parents[1]
sys.path.append(osp.join(parentdir, 'scripts'))

from utils import get_best_word, read_words


def play_wordle(words_list, pwm):
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

    # Open chrome to wordle website
    driver = webdriver.Chrome('chromedriver')
    shadow = Shadow(driver)
    driver.get("https://www.nytimes.com/games/wordle/index.html")

    # Close the pop-up menu with game instructions
    button = shadow.find_elements('.close-icon')
    button[0].click()

    # navigate to the keyboard
    keyboard = shadow.find_element('#keyboard')

    # guess words until solved or out of guesses
    solved = False 
    attempt = 0
    while not solved and attempt < 6:

        word = get_best_word(words_list, pwm, letters_by_pos, present_letters)['word']

        # Type best word and enter
        for char in word:
            letter = shadow.find_element(keyboard, f'button[data-key="{char}"]')
            letter.click()
        submit = shadow.find_element(keyboard, f'button[data-key="↵"]')
        submit.click()
        attempt += 1

        # update valid letters
        board = shadow.find_element('#board')
        game_row = shadow.find_element(board, f'game-row[letters="{word}"]')

        # need to iterate through the tiles to preserve position if duplicate letters
        div_row = shadow.find_element(game_row, '.row')
        tiles = shadow.get_child_elements(div_row)

        solved = True
        for pos, tile in enumerate(tiles):
            letter = shadow.get_attribute(tile, 'letter')
            eval = shadow.get_attribute(tile, 'evaluation')
    
            if eval == 'present':
                solved = False
                # remove the letter from this pos (since not correct)
                if letter in letters_by_pos[pos]: letters_by_pos[pos].remove(letter)

                # send a flag signalling this letter MUST be in the word
                present_letters.append(letter)
            
            elif eval == 'correct':
                # this position can only be the letter
                letters_by_pos[pos] = [letter]

            # eval == absent
            else:
                solved = False
                # remove the letter from each pos
                for pos in letters_by_pos:
                    if letters_by_pos[pos] == [letter]: continue
                    elif letter in letters_by_pos[pos]: letters_by_pos[pos].remove(letter)
        
        time.sleep(3)

    if solved:
        print(f"Wordle-bot solved today's wordle in {attempt} tries!")
    else:
        print("Wordle-bot couldn't solve today's wordle :(")
    
    time.sleep(5)
    # Close the tab when finished
    driver.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--words')
    parser.add_argument('-p', '--pwm')

    args = parser.parse_args()
    words_file = args.words
    pwm_file = args.pwm

    words_list = read_words(words_file)

    # NOTE: json.load() automatically converts keys into strings, thus they are no longer ints!
    pwm = json.load(open(pwm_file, 'r'))

    play_wordle(words_list, pwm)


if __name__ == '__main__':
    main()