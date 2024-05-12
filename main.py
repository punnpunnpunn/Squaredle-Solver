import pygame as pg
import time
import math
from project import *

word_tree = Tree('Start')

with open('dictionary.txt') as word_dict:
    for line in word_dict.readlines():
        line_stripped = line.strip()
        if len(line_stripped) >= 4:
            word_tree.add_string(line_stripped)
squaredle = make_squaredle(input("Which squaredle would you like to play (ex. yesterday.txt):\n"))
graph = Squaredle(squaredle)
WORD_LIST = find_words(graph, word_tree)
pg.init()
SQUAREDLE_SIZE = len(squaredle)
SQUARE_SPACE = math.floor(425/(SQUAREDLE_SIZE+1))
SCREEN_WIDTH = 1200
FOUND_WORDS = ['']
SCREEN_HEIGHT = 800
LETTER_SIZE = SQUARE_SPACE - 10
font = pg.font.get_default_font()
FONT = pg.font.Font(font, LETTER_SIZE- math.floor(LETTER_SIZE/3))
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
square_positions = []
square_positions_b = []
square_colors = []
square_colors_b = []
to_rc = {}
for key in graph.vertices:
    to_rc[graph.vertices[key]] = key
word_dic = set()
with open("dictionary.txt") as dic:
    lines = dic.readlines()
    for line in lines:
        word_dic.add(line.strip())
for r in range(len(squaredle)):
    square_positions.append([])
    square_colors.append([])
    square_positions_b.append([])
    square_colors_b.append([])
    for c in range(len(squaredle[r])):
        square_positions[r].append((100 + math.floor(SQUARE_SPACE/2) + r*(SQUARE_SPACE), 100 +  math.floor(SQUARE_SPACE/2) + c*(SQUARE_SPACE)))
        square_colors[r].append((255, 255, 255))
        square_positions_b[r].append((600 + math.floor(SQUARE_SPACE/2) + r*(SQUARE_SPACE), 100 +  math.floor(SQUARE_SPACE/2) + c*(SQUARE_SPACE)))
        square_colors_b[r].append((255, 255, 255))
show_font = pg.font.Font(font, 50)
find_font = pg.font.Font(font, 30)


def _draw_letter(screen: pg.Surface, letter: str, bg_x: int, bg_y: int, color: tuple) -> None:
    """Draw a letter on the screen at the given position. Letters are automatically converted to uppercase.
    """
    bg_rect = (bg_x, bg_y, LETTER_SIZE, LETTER_SIZE)
    bg_colour = color
    text_position = (bg_x + LETTER_SIZE // 2, bg_y + LETTER_SIZE // 2)
    text_screen = FONT.render(str.upper(letter), True, (0, 0, 0))
    text_rect = text_screen.get_rect(center=text_position)
    pg.draw.rect(screen, bg_colour, bg_rect, 0, 10)
    screen.blit(text_screen, text_rect)




def in_square(pos: tuple[int]) -> tuple[int]:
    """Checks if the coordinates pos is close to one of the squares in square_positions"""
    for r in range(len(square_positions)):
        for c in range(len(square_positions[r])):
            if abs(pos[0] - square_positions[r][c][1]) < ((LETTER_SIZE -25)/2 + 1) and abs(pos[1] - square_positions[r][c][0]) < ((LETTER_SIZE -25)/2 + 1):
                return (r, c)
    return (-1, -1)

def are_neighbors(p: tuple, q: tuple) -> bool:
    """Checks if letters p and q are neighbors"""
    for i in range(-1, 2):
        for j in range(-1, 2):
            if p == (q[0] + i, q[1] + j):
                return True
    return False

def reset_colors() -> None:
    """Resets the square colors to white"""
    for r in range(len(square_colors)):
        for c in range(len(square_colors)):
            square_colors[r][c] = (255, 255, 255)



def show_find_words(squaredle_graph, word_tree) -> set:
    """ Returns the words in the squaredle"""
    wordbank = []
    for letter in squaredle_graph.vertices.values():
        if letter.value != '#' and letter.value not in word_tree.subtrees:
            raise ValueError
        elif letter.value != '#':
            wordbank += show_find_words_with_start(letter.value, letter, squaredle_graph, word_tree.subtrees[letter.value], [letter], FOUND_WORDS)
    return set(wordbank)

def refresh(string_a, string_b) -> None:
    """ Refreshed the screen """
    screen.fill((7, 74, 148))
    pg.draw.rect(screen, (40, 42, 94), pg.Rect(square_positions[0][0][0] -SQUARE_SPACE, square_positions[0][0][1]-SQUARE_SPACE, 425, 425), 0, 10)
    pg.draw.rect(screen, (173, 46, 36), pg.Rect(square_positions_b[0][0][0] -SQUARE_SPACE, square_positions_b[0][0][1]-SQUARE_SPACE, 425, 425), 0, 10)
    for r in range(len(squaredle)):
        for c in range(len(squaredle[r])):
            _draw_letter(screen, squaredle[r][c], 100 + c*SQUARE_SPACE, 100 + r*SQUARE_SPACE, square_colors[r][c])
            _draw_letter(screen, squaredle[r][c], 600 + c*SQUARE_SPACE, 100 + r*SQUARE_SPACE, square_colors_b[r][c])
    text = find_font.render(FOUND_WORDS[0], True, (0, 0, 0) ,(7, 74 , 148))
    textRect = text.get_rect()
    textRect.center = (300, 650)
    screen.blit(text, textRect)  
    text = show_font.render(string_a, True, (0, 0, 0) ,(7, 74 , 148))
    textRect = text.get_rect()
    textRect.center = (300, 600)
    screen.blit(text, textRect)  
    text = show_font.render(string_b, True, (0, 0, 0) ,(7, 74 , 148))
    textRect = text.get_rect()
    textRect.center = (900, 600)
    screen.blit(text, textRect)  
    pg.display.update()

def delay(x) -> None:
    """ Delays [Max idk what this does]"""
    start = time.time()
    while (time.time() - start < x):
        start = start

def show_find_words_with_start(string, letter, squaredle_graph, word_tree, used_letters, found_wordlist) -> list:
    """ Returns all the words in the squaredle that starts with string without using used_letters """
    wordlist = []
    refresh(string, '')
    delay(.01)
    square_colors[to_rc[letter][0]][to_rc[letter][1]] = (121, 126, 232)
    if "END" in word_tree.subtrees:
        found_wordlist[0] = string 
        wordlist = [string]
    for l in letter.neighbours:
        if l not in used_letters and l.value in word_tree.subtrees:
            wordlist += show_find_words_with_start(string + l.value, l, squaredle_graph, word_tree.subtrees[l.value], used_letters + [l], found_wordlist)
    square_colors[to_rc[letter][0]][to_rc[letter][1]] = (255, 255, 255)
    refresh(string, '')
    delay(.01)
    return wordlist


def show_both(squaredle_graph, words, word_tree) -> None:
    """Shows both ways of solving the squaredle (by brute force and by using graphs and trees)"""
    a_stack = [(0, -1, 0, 0, '')]
    b_stack = [(0, -1, 0, '')]
    a_words = []
    b_words = []
    for letter in squaredle_graph.vertices.values():
        if letter.value != '#' and letter.value not in word_tree.subtrees:
            raise ValueError
        elif letter.value != '#':
            a_stack.append((letter, 0, word_tree.subtrees[letter.value], [letter], letter.value))
    for letter in squaredle_graph.vertices.values():
        b_stack.append((letter, 0, [letter], letter.value))
    a = a_stack.pop()
    b = b_stack.pop()
    while a_stack or b_stack:
        if a[1] == -1:
            reset_colors()
        if a[2] != 0 and 'END' in a[2].subtrees:
            a_words.append(a[4])
        if len(b[3]) > 3 and b[3] in words:
            b_words.append(b[3])
        if a[2] != 0:
            square_colors[to_rc[a[0]][0]][to_rc[a[0]][1]] = (121, 126, 232)
        if b[1] != -1:
            square_colors_b[to_rc[b[0]][0]][to_rc[b[0]][1]] = (191, 115, 109)
        refresh(a[4], b[3])
        delay(.01)
        for l in b[0].neighbours:
            if l not in b[2]:
                b_stack.append((l, b[1] + 1, b[2] + [l], b[3] + l.value))
        if a[1] != -1:
            for l in a[0].neighbours:
                if l not in a[3] and l.value in a[2].subtrees:
                    a_stack.append((l, a[1] + 1, a[2].subtrees[l.value], a[3] + [l], a[4] + l.value))
        if a_stack:
            temp = a_stack.pop()
            if temp[1] <= a[1]:
                square_colors[to_rc[a[0]][0]][to_rc[a[0]][1]] = (255, 255, 255)
            a = temp
        if b_stack:
            temp = b_stack.pop()
            if temp[1] <= b[1] and temp[1] != -1:
                square_colors_b[to_rc[b[0]][0]][to_rc[b[0]][1]] = (255, 255, 255)
            b = temp
        refresh(a[4], b[3])
        delay(.01)
    print(b_words)
    print(a_words)
        
#show_both(graph, word_dic, word_tree)

def run() -> None:
    """ Runs the pygame """
    run = True
    word = ''
    visited = set()
    past_rc = (-1, -1)
    already_found = []
    screen.fill((7, 74, 148))
    start = 0
    while run:
        if word == '' and (time.time() - start) > 2:
            screen.fill((7, 74, 148))
        pg.draw.rect(screen, (40, 42, 94), pg.Rect(square_positions[0][0][0] -SQUARE_SPACE, square_positions[0][0][1]-SQUARE_SPACE, 425, 425), 0, 10)
        if pg.mouse.get_pressed()[0]:
            rc = in_square(pg.mouse.get_pos())
            if all({rc != (-1, -1), rc not in visited, (are_neighbors(rc, past_rc) or past_rc == (-1, -1))}):
                screen.fill((7, 74, 148))
                pg.draw.rect(screen, (40, 42, 94), pg.Rect(square_positions[0][0][0] -SQUARE_SPACE, square_positions[0][0][1]-SQUARE_SPACE, 425, 425), 0, 10)
                square_colors[rc[0]][rc[1]] = (121, 126, 232)
                word += squaredle[rc[0]][rc[1]]
                text = find_font.render(word, True, (0, 0, 0) ,(110, 110, 140))
                textRect = text.get_rect()
                textRect.center = (400, 30)
                screen.blit(text, textRect)  
                visited.add(rc)
                past_rc = rc
        else:
            if word != '':
                response = check_word(word, WORD_LIST, already_found)
                text = find_font.render(response, True, (0, 0, 0) ,(110, 110, 140))
                textRect = text.get_rect()
                textRect.center = (400, 30)
                screen.blit(text, textRect)
                start = time.time()
            if word in WORD_LIST and word not in already_found:
                already_found.append(word)
            reset_colors()
            past_rc = (-1, -1)
            visited = set()
            word = ''
        for r in range(len(squaredle)):
            for c in range(len(squaredle[r])):
                _draw_letter(screen, squaredle[r][c], 100 + c*SQUARE_SPACE, 100 + r*SQUARE_SPACE, square_colors[r][c])
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        pg.display.update()
    pg.quit()

def solve_play_or_compare():
    """get text input to either play, solve, or compare the squaredle"""
    print("Type 'solve' to show a visualization of our algorithm")
    print("Type 'play' to play the squaredle")
    print("Type 'compare' to show a visualization of our algorithm and the brute force algorithm")
    print()
    x = input("What to do:")
    if x == "solve":
        found_words = show_find_words(graph, word_tree)
        print(found_words)
        print(len(found_words))
    elif x == "play":
        run()
    elif x == "compare":
        show_both(graph, word_dic, word_tree)
    else:
        raise ValueError

solve_play_or_compare()

