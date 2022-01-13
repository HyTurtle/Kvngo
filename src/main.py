from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty

kv = '''
#:import r random.random
<CLabel@Label>:
    colour: r(), r(), r()
    font_size: sp(24)
    state: 'normal'
    canvas.before:
        Color:
            rgba: (*self.colour[::-1], (1,.1)[self.disabled or self.state == 'down']) if self.colour else (0, 0, 0, 0)
        Rectangle:
            pos: self.x - 3, self.y - 3 
            size: self.width + 6, self.height + 6
        Color:
            rgba: (*self.colour, (1,.1)[self.disabled or self.state == 'down']) if self.colour else (0, 0, 0, 0)
        Rectangle:
            pos: self.pos
            size: self.size
        

<Attempt@BoxLayout>:
    spacing: sp(10)
    CLabel:
        text: ''
    CLabel:
        text: ''
    CLabel:
        text: ''
    CLabel:
        text: ''
    CLabel:
        text: ''

<Board@BoxLayout>:
    orientation: 'vertical'
    spacing: sp(10)
    Attempt
    Attempt:
        disabled: True
    Attempt:
        disabled: True
    Attempt:
        disabled: True
    Attempt:
        disabled: True

<CButton@ButtonBehavior+CLabel>:
    color: 0,0,0,1
    #colour: .6,.7,.3
    on_release: app.pressed(self)

<Keys@BoxLayout>:
    orientation: 'vertical'
    spacing: dp(8)
    BoxLayout:
        spacing: dp(8)
        CButton:
            text: 'q'
        CButton:
            text: 'w'
        CButton:
            text: 'e'
        CButton:
            text: 'r'
        CButton:
            text: 't'
        CButton:
            text: 'y'
        CButton:
            text: 'u'
        CButton:
            text: 'i'
        CButton:
            text: 'o'
        CButton:
            text: 'p'
    BoxLayout:
        spacing: dp(8)
        #Widget:
        #    width: cb.width//2
        CButton:
            id: cb
            text: 'a'
        CButton:
            text: 's'
        CButton:
            text: 'd'
        CButton:
            text: 'f'
        CButton:
            text: 'g'
        CButton:
            text: 'h'
        CButton:
            text: 'j'
        CButton:
            text: 'k'
        CButton:
            text: 'l'
        CButton:
            text: '<-'
        #Widget:
        #    width: cb.width//2
    BoxLayout:
        spacing: dp(8)
        Widget:
            width: cb.width * 1.5
        CButton:
            id: cb2
            text: 'z'
        CButton:
            text: 'x'
        CButton:
            text: 'c'
        CButton:
            text: 'v'
        CButton:
            text: 'b'
        CButton:
            text: 'n'
        CButton:
            text: 'm'
        Widget:
            width: cb.width * 1.5

Screen:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)
        pos_hint: {'center_x': .5}
        Board:
            id: board
            size_hint_y: .7
        Keys
            size_hint_y: .3
'''


class Lingo(App):
    guesses = ListProperty()

    def build(self):
        return Builder.load_string(kv)

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
