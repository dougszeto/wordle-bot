import math
import tweepy
from dotenv import dotenv_values
from pathlib import Path
import os.path as osp

parentdir = Path(__file__).parents[1]

# all possible outcomes of a guess
combos = []
states = [ 'absent', 'present', 'correct']
for i in states:
    for j in states:
        for k in states:
            for l in states:
                for m in states:
                    combos.append((i,j,k,l,m))


def solver_version_1(all_words, letters_by_pos, present_letters):
    valid_words = filter_words(letters_by_pos, all_words, present_letters)
    pwm = calc_pwm(valid_words)
    return get_most_probable_word(valid_words, pwm)


def get_best_word(all_words, letters_by_pos, present_letters):
    # step 1: filter all words to contain only words that use exclusively valid_letters -> valid_words

    valid_words = filter_words(letters_by_pos, all_words, present_letters)
    pwm = calc_pwm(valid_words)

    # step 2: iterate through valid_words and use PWM to get top 10 most probable words
    most_probable_words = []
    if len(valid_words) > 10:
        for i in range(10):
            best = get_most_probable_word(valid_words, pwm)
            most_probable_words.append(best)
            valid_words.remove(best)        # need to remove best so that we don't get same result 10 times
    else: most_probable_words = valid_words

    
    # step 3: iterate through top 10 most probable words and choose the one with most information
    best_word = get_most_info_word(most_probable_words, all_words)
    return best_word

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

def calc_info(word, all_words):
    expected_info = 0
    letters_by_pos = {
        0: [chr(i) for i in range(97, 123)],
        1: [chr(i) for i in range(97, 123)],
        2: [chr(i) for i in range(97, 123)],
        3: [chr(i) for i in range(97, 123)],
        4: [chr(i) for i in range(97, 123)]
    }
    present_letters = []
    # calculate prob of all 3^5 (number of words that satisfy pattern / total words)
    for combo in combos:
        for pos, state in enumerate(combo):
            letter = word[pos]
            if state == 'present' and letter in letters_by_pos[pos]:
                letters_by_pos[pos].remove(letter)
                present_letters.append(letter)
            elif state == 'correct': letters_by_pos[pos] = [letter]
            else:
                for pos in letters_by_pos:
                    if letters_by_pos[pos] == [letter]: continue
                    elif letter in letters_by_pos[pos]: letters_by_pos[pos].remove(letter)
        
        filtered_words = filter_words(letters_by_pos, all_words, present_letters)
        combo_prob = len(filtered_words) / len(all_words)

        # calculate expected information E(x) = sum(prob(x) * -log2(p(x)))
        if combo_prob > 0:
            expected_info += (combo_prob * -math.log(combo_prob, 2))

    return expected_info

    
def get_most_probable_word(words, pwm):
    best_word = ''
    best_prob = 0
    for word in words:
        prob = 1
        for pos, char in enumerate(word):
            prob *= pwm[pos][char]
            if prob > best_prob:
                best_word = word
                best_prob = prob

    return best_word

def get_most_info_word(query_words, all_words):
    best_info = 0
    best_word = ''
    for query in query_words:
        info = calc_info(query, all_words)
        if info > best_info:
            best_info = info
            best_word = query
    return best_word

