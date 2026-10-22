"""Shine Forever — an animated celestial scene for your terminal."""

import os
import random
import shutil
import sys
import time

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
BLUE = "\033[38;5;75m"
CYAN = "\033[38;5;117m"
GOLD = "\033[38;5;220m"
WHITE = "\033[38;5;255m"
PURPLE = "\033[38;5;141m"

MOON = [
    "              .-''''-.              ",
    "           .-'  .--.  '-.           ",
    "         .'   .'    '.   '.         ",
    "        /   .'  .--.  '.   ",
    "       ;   /   /      \\   ;",
    "       |  ;   |  o  o  |   |",
    "       ;   \\   \\      /   ;",
    "        \\   '.  '--'  .'   /",
    "         '.   '.    .'   .'",
    "           '-.  '--'  .-'",
    "              '-....-'",
]

SUN = [
    "             |  |  |             ",
    "          '.  |  |  .'             ",
    "        ---- .-***-. ----        ",
    "          .'  *****  '.          ",
    "         /  *********  /",
    "        |  ***********  |",
    "         \\  *********  /",
    "          '.  *****  .'",
    "        ---- '-***-' ----        ",
    "          .'  |  |  '.          ",
    "             |  |  |             ",
]


def make_stars(width, height, count):
    stars = {}
    symbols = [".", "·", "✦", "+", "*", "˚"]
    for _ in range(count):
        stars[(random.randrange(width), random.randrange(height))] = random.choice(symbols)
    return stars


def render(frame):
    size = shutil.get_terminal_size((80, 24))
    width = min(size.columns, 100)
    height = max(18, min(size.lines - 2, 32))
    canvas = [[" " for _ in range(width)] for _ in range(height)]

    for (x, y), symbol in make_stars(width, height, max(30, width // 2)).items():
        if y < height - 5:
            canvas[y][x] = symbol

    art = MOON if (frame // 18) % 2 == 0 else SUN
    art_color = BLUE if art is MOON else GOLD
    start_y = max(1, (height - len(art)) // 2 - 1)
    start_x = max(0, (width - max(map(len, art))) // 2)

    for row, line in enumerate(art):
        for col, char in enumerate(line):
            x, y = start_x + col, start_y + row
            if 0 <= x < width and 0 <= y < height and char != " ":
                canvas[y][x] = char

    sys.stdout.write("\033[H")
    for y, row in enumerate(canvas):
        output = ""
        for x, char in enumerate(row):
            if char in ".·✦+*˚":
                output += random.choice([DIM + BLUE, CYAN, PURPLE, WHITE]) + char + RESET
            elif start_y <= y < start_y + len(art) and start_x <= x < start_x + max(map(len, art)) and char != " ":
                output += art_color + BOLD + char + RESET
            else:
                output += char
        print(output)

    print("\n" + PURPLE + BOLD + "✦  SHINE FOREVER  ✦".center(width) + RESET)
    print(CYAN + DIM + "even the darkest sky has a little light".center(width) + RESET)
    print(DIM + "Press Ctrl+C to let the stars rest.".center(width) + RESET)


def main():
    if os.name == "nt":
        os.system("")  # Enable ANSI escape sequences in modern Windows consoles.
    sys.stdout.write("\033[2J\033[?25l")
    try:
        frame = 0
        while True:
            render(frame)
            frame += 1
            time.sleep(0.22)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h" + RESET + "\n")
        print(GOLD + "Keep shining. ✨" + RESET)


if __name__ == "__main__":
    main()
