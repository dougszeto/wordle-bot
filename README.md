# Wordle-Bot
## Setup
Install conda and then run
`conda create --name <env> --file requirements.txt` to geneate a new conda environment with required packages

## To Run
Make sure to download the [chrome driver](https://chromedriver.chromium.org/downloads) and add it your PATH. Then navigate to the root of this project and run 
`python src/main.py -w data/all-words.txt -p data/pwm.json`
## File Structure
```
wordle-bot
├── src
    ├── main.py
├── scripts
    ├── calc_freq.py (used to generate data/pwm.json)
    ├── utils.py (includes helper functions)
├── data
    ├── all-words.txt 
    ├── pwm.json
├── requirements.txt
├── READEME.md
```
Note that `data/all-words.txt` was retrieved from  [https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt](https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt) and is not an exhaustive list of all 5 letter words in the English dictionary.

## Future Improvements
* Create a scheme to score potential words based on how much info they reveal (ie. reward words without duplicate letters)
* Use more extensive list of words for `data/all-words.txt`
* ~~Connect to Twitter API / SMS / Email to share results?~~