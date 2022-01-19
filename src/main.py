from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import ListProperty, StringProperty
from random import choice
import words

class Lingo(App):
    guesses = ListProperty()
    answer = StringProperty('')

    def pressed(self, button):
        for r_index, row in enumerate(self.root.ids.board.children[::-1]):
            for index, i in enumerate(row.children[::-1]):
                if not i.text:
                    if button.text != '<-':
                        i.text = button.text.upper()
                    elif index:
                        row.children[::-1][index - 1].text = ''
                        return
                    if index == 4:
                        self.check_row(row)
                        if r_index != 4:
                            self.root.ids.board.children[::-1][r_index+1].disabled = False
                        else:
                            print('failed')
                    return

    def check_row(self, row):
        guess = ''
        for r in row.children[::-1]:
            guess += r.text
            if r.text.upper() in self.answer:
                r.valid = True
        self.guesses.append(guess.upper())
        self.mark_keys(guess)

    def get_word(self, difficulty: str = 'easy'):
        self.answer = choice(getattr(words, difficulty)).upper()
        print(self.answer)

    def on_start(self):
        self.get_word()

    def mark_keys(self, guess:str):
        for char in guess:
            for key in filter(lambda i: isinstance(i, Label), self.root.ids.qwe.walk()):
                if key.text == char.lower():
                    if char in self.answer:
                        key.present = True
                    else:
                        key.disabled = True

    def on_guesses(self, inst, values):
        if values[-1] == self.answer:
            print('Correct')


if __name__ == '__main__':
    Lingo().run()
