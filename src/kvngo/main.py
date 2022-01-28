from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.properties import ListProperty, StringProperty, OptionProperty
from kivy.animation import Animation
from random import choice
from . import words


class GameScreen(Screen):
    guesses = ListProperty()
    answer = StringProperty('')
    difficulty = OptionProperty('easy', options=['easy', 'hard'])

    def pressed(self, button):
        for r_index, row in enumerate(self.ids.board.children[::-1]):
            for index, i in enumerate(row.children[::-1]):
                if not i.text:
                    if button.text != '<-':
                        if not i.disabled:
                            i.text = button.text.upper()
                    elif index:
                        row.children[::-1][index - 1].text = ''
                        return
                    else:
                        self.ids.board.children[::-1][r_index-1].children[index].text = ''
                        return
                    if index == 4:
                        if not self.check_row(row):
                            anim = Animation(x=row.x+20, d=.15) + Animation(x=row.x-20, d=.3) + Animation(x=row.x, d=.1)
                            anim.start(row)
                            return
                        if r_index != 4:
                            self.ids.board.children[::-1][r_index+1].disabled = False
                        else:
                            print('failed')
                    return

    def check_row(self, row):
        guess = ''.join(r.text for r in row.children[::-1])
        if guess.lower() in getattr(words, self.difficulty):
            for r in row.children:
                if r.text in self.answer:
                    r.valid = True
            self.guesses.append(guess)
            self.mark_keys(guess)
            return True
        else:
            return False

    def get_word(self):
        self.answer = choice(getattr(words, self.difficulty)).upper()
        print(self.answer)

    def mark_keys(self, guess: str):
        for char in guess:
            for key in filter(lambda i: isinstance(i, Label), self.ids.qwe.walk()):
                if key.text == char.lower():
                    if char in self.answer:
                        key.present = True
                    else:
                        key.disabled = True

    def on_guesses(self, inst, values):
        if values[-1] == self.answer:
            self.ids.qwe.disabled = True
            Clock.schedule_once(lambda _: setattr(self.manager, 'current', 'menu'), 3)

    def on_pre_enter(self):
        self.get_word()

    def on_leave(self):
        for key in filter(lambda widget: isinstance(widget, Label), self.ids.qwe.walk()):
            key.disabled = False
            key.present = False
            self.ids.qwe.disabled = False
        for r_index, row in enumerate(self.ids.board.children[::-1]):
            if r_index:
                row.disabled = True
            for index, i in enumerate(row.children[::-1]):
                if i.text:
                    i.valid = False
                    i.text = ''
                else:
                    return


class Kvngo(App):
    ...


def run():
    Kvngo().run()


if __name__ == '__main__':
    run()
