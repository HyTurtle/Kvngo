from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty


class Lingo(App):
    guesses = ListProperty()

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
        guess = ''.join([r.text for r in row.children[::-1]])
        self.guesses.append(guess)
        print(guess)


Lingo().run()
