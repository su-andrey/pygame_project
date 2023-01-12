import pygame as pg
import pygame.freetype as freetype
import main as mn
import json

PRINT_EVENT = False
CHATLIST_POS = pg.Rect(0, 20, 1150, 400)
CHATBOX_POS = pg.Rect(0, 440, 1150, 40)



pg.init()
Screen = pg.display.set_mode((1400, 1000))
FPSClock = pg.time.Clock()

Font = freetype.SysFont('arial', 24)


def main(some_text):
    global BGCOLOR, PRINT_EVENT, CHATBOX_POS, CHATLIST_POS, CHATLIST_MAXSIZE
    global FPSClock, Font, Screen
    pg.key.start_text_input()
    input_rect = pg.Rect(80, 80, 320, 40)
    pg.key.set_text_input_rect(input_rect)

    _IMEEditing = False
    _IMEText = ""
    _IMETextPos = 0
    _IMEEditingText = ""
    _IMEEditingPos = 0
    ChatList = []
    tex = 1
    while tex:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if _IMEEditing:
                    if len(_IMEEditingText) == 0:
                        _IMEEditing = False
                    continue
                if event.key == pg.K_BACKSPACE:
                    if len(_IMEText) > 0 and _IMETextPos > 0:
                        _IMEText = (
                                _IMEText[0: _IMETextPos - 1] + _IMEText[_IMETextPos:]
                        )
                        _IMETextPos = max(0, _IMETextPos - 1)
                elif event.key == pg.K_DELETE:
                    _IMEText = _IMEText[0:_IMETextPos] + _IMEText[_IMETextPos + 1:]
                elif event.key == pg.K_LEFT:
                    _IMETextPos = max(0, _IMETextPos - 1)
                elif event.key == pg.K_RIGHT:
                    _IMETextPos = min(len(_IMEText), _IMETextPos + 1)
                elif event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
                    if len(_IMEText) == 0:
                        continue
                    # Append chat list
                    ChatList.append(_IMEText)

                    tex = 0
                    return _IMEText


            elif event.type == pg.TEXTEDITING:
                if PRINT_EVENT:
                    print(event)
                _IMEEditing = True
                _IMEEditingText = event.text
                _IMEEditingPos = event.start

            elif event.type == pg.TEXTINPUT:
                if PRINT_EVENT:
                    print(event)
                _IMEEditing = False
                _IMEEditingText = ""
                _IMEText = _IMEText[0:_IMETextPos] + event.text + _IMEText[_IMETextPos:]
                _IMETextPos += len(event.text)


        Screen.fill('black')
        draw_text(some_text)

        # Chat box updates
        start_pos = CHATBOX_POS.copy()
        ime_textL = ">" + _IMEText[0:_IMETextPos]
        ime_textM = (
                _IMEEditingText[0:_IMEEditingPos] + "|" + _IMEEditingText[_IMEEditingPos:]
        )
        ime_textR = _IMEText[_IMETextPos:]

        rect_textL = Font.render_to(Screen, start_pos, ime_textL, 'green')
        start_pos.x += rect_textL.width

        # Editing texts should be underlined
        rect_textM = Font.render_to(
            Screen, start_pos, ime_textM, 'green', None, freetype.STYLE_UNDERLINE
        )
        start_pos.x += rect_textM.width
        Font.render_to(Screen, start_pos, ime_textR, 'green')

        pg.display.update()

def draw_text(text):
    if 'records' in text and 'Введите' not in text:
        with open('data/res.json') as cat_file:
            data = json.load(cat_file)
        if text[-2:] == ' 0':
            print(data)
        else:
            ind = (text[-2:]).strip()
            if len(data[ind]) > 10:
                res = ' '.join(sorted(data[ind])[:10])
                res += f' {data[ind][-1]}'
            else:
                res = ' '.join(data[ind])
            print(res)
    else:
        font = pg.font.Font(pg.font.match_font('arial'), 30)
        text_surface = font.render(text, True, 'green')
        text_rect = text_surface.get_rect()
        text_rect.x = 0
        Screen.blit(text_surface, text_rect)