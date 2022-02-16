from hashlib import new
from selenium import webdriver
from pyshadow.main import Shadow
from datetime import date

class NYTimesConnector:
    driver = webdriver.Chrome('chromedriver')
    shadow = Shadow(driver)

    def start(self):
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
    
    def close_instructions(self):
        button = self.shadow.find_elements('.close-icon')
        button[0].click()

    def submit_guess(self, guess):
        # enter the guess on the keyboard
        keyboard = self.shadow.find_element('#keyboard')
        for char in guess:
            letter = self.shadow.find_element(keyboard, f'button[data-key="{char}"]')
            letter.click()
        submit = self.shadow.find_element(keyboard, f'button[data-key="↵"]')
        submit.click()

        # return each letter and it's evaluation (present, absent, or correct)
        response = []
        board = self.shadow.find_element('#board')
        game_row = self.shadow.find_element(board, f'game-row[letters="{guess}"]')
        div_row = self.shadow.find_element(game_row, '.row')
        tiles = self.shadow.get_child_elements(div_row)

        for tile in tiles:
            letter = self.shadow.get_attribute(tile, 'letter')
            eval = self.shadow.get_attribute(tile, 'evaluation')
            response.append((letter, eval))
        return response

    def score_header(self, attempt):
        d0 = date(2022, 2, 16)
        d1 = date.today()
        days = (d1-d0).days
        wordle_number = 242 + days
        return f'Wordle {wordle_number} {attempt}/6\n\n'

    def exit(self):
        self.driver.close()
        
# ny_times = NYTimesConnector()
# ny_times.close_instructions()
# response = ny_times.submit_guess("touch")
# ny_times.exit()

# print(response)