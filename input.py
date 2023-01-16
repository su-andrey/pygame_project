import time

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


def custom_draw(text, size, hard_level, y=100):
    if type(text) == list:
        text1, text2 = text[0], text[1]
    font = pg.font.Font(pg.font.match_font('arial'), size)
    font_small = pg.font.Font(pg.font.match_font('arial'), int(size * 0.8))
    if type(text) != list:
        text_surface_for_hard_level = font_small.render(f'Дорогой игрок, вот твои рекорды за {hard_level} '
                                                        f'уровень сложности', True, 'green')
        text_surfZace = font.render(text, True, 'green')
    else:
        text_surface_for_hard_level = font.render(text1, True, 'green')
        text_surface = font.render(text2, True, 'green')
    text_rect_for_hard_level = text_surface_for_hard_level.get_rect()
    text_rect_for_hard_level.x = 0
    text_rect = text_surface.get_rect()
    text_rect.x, text_rect.y = 0, y
    Screen.blit(text_surface_for_hard_level, text_rect_for_hard_level)
    Screen.blit(text_surface, text_rect)
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                exit()
            if event.type == pg.QUIT:
                exit()


def draw_text(text):
    if 'records' in text and 'Введите' not in text:
        with open('data/res.json') as cat_file:
            data = json.load(cat_file)
        res = ['', '']
        ind = (text[-2:]).strip()
        if ind == '0':
            for i in range(1, 11):
                try:
                    res[(i - 1) // 5] += (f'Cложность {i}: {data[str(i)][0]}мин; ')
                except IndexError:
                    res[(i - 1) // 5] += (f'Cложность{i}: пусто! ')
            custom_draw(res, 30, res, 50)
        else:
            try:
                if len(data[ind]) > 10:
                    res = 'мин '.join(sorted(data[ind])[:10])
                    res += f'мин {data[ind][-1]}мин'
                    custom_draw(res, Screen.get_size()[0] // 32, ind)
                else:
                    res = 'мин '.join(data[ind])
                    if res:
                        res += 'мин'
                    if res:
                        custom_draw(res, Screen.get_size()[0] // (len(res) + 15), ind)
                    else:
                        res = ['Пока нет рекорда в этом режиме. Если Вы хотите установить его', f'То при выборе режима '
                                                                                    f'сложности напишите {ind}']
                        custom_draw(res, 35, ind)
            except KeyError:
                exit()
    else:
        font = pg.font.Font(pg.font.match_font('arial'), 30)
        text_surface = font.render(text, True, 'green')
        text_rect = text_surface.get_rect()
        text_rect.x = 0
        Screen.blit(text_surface, text_rect)
