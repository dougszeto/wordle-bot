import tweepy
from dotenv import dotenv_values
from pathlib import Path
import os.path as osp

parentdir = Path(__file__).parents[1]

# NOTE: consider adding a penalty for repeating letters and collecting the top 10 words and deciding which gives most info
def get_best_word(all_words, letters_by_pos, present_letters):
    # step 1: filter all words to contain only words that use exclusively valid_letters -> valid_words

    valid_words = filter_words(letters_by_pos, all_words, present_letters)
    pwm = calc_pwm(valid_words)

    # step 2: iterate through valid_words and calculate probabilities using PWM
    best = {
        'word': '',
        'prob': 0
    }
    for word in valid_words:
        prob = 1
        for pos, char in enumerate(word):
            prob *= pwm[pos][char]
        if prob > best['prob']:
            best['word'] = word
            best['prob'] = prob
    
    # step 3: select and return the most probable word
    return best

def filter_words(letters_by_pos, words, present_letters):
    valid_words = []
    for word in words:
        valid = True

        # check if it contains present letters
        for present_letter in present_letters:
            if present_letter not in word:
                valid = False
                break

        # check each character of the word to see if it can be in it's current position
        for pos, char in enumerate(word):
            if char not in letters_by_pos[pos]:
                valid = False
                break
        
        if valid:
            valid_words.append(word)
    return valid_words
        
def read_words(word_file):
    all_words = []
    with open(word_file, 'r') as fp:
        lines = fp.readlines()

        # for every line except the last
        for line in lines[:-1]:
            word = line[:-1]
            word = word.lower()
            all_words.append(word)

        last_word = lines[-1].lower()
        all_words.append(last_word)
    return all_words


def tweet_score(score):
    config = dotenv_values(osp.join(parentdir, '.env'))

    client = tweepy.Client(
        consumer_key=config['CONSUMER'],
        consumer_secret=config['CONSUMER_SECRET'],
        access_token=config['ACCESS'],
        access_token_secret=config['ACCESS_SECRET']
    )
    client.create_tweet(text=score)

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