import sys
from cubescrambler import scrambler666
import magiccube

def print_help():
    print("Welcome to the 6BLD Memo Maker!")
    print("-s [scramble] (default: makes its own scramble)")

    # buffer selection
    print("-oxc [buffer]") # outer x centers
    print("-ixc [buffer]") # inner x centers
    print("-co [buffer]") # clockwise obliques
    print("-cc [buffer]") # counterclockwise obliques
    print("-ow [buffer]") # outer wings
    print("-iw [buffer]") # inner wings
    print("-c [buffer]") # corners
    print()
    print("Alternatively, for full custom buffer selection:")
    print("-b abcdefg") # a = buffer for outer x centers, b = buffer for inner x centers, etc.


def parse_cube(cube_str):
    lines = cube_str.strip().split('\n')

    # Strip and split each line into characters
    grid = [list(line.strip()) for line in lines]

    # Extract faces
    top = [grid[i][6:12] for i in range(0, 6)]
    left = [grid[i][0:6] for i in range(6, 12)]
    front = [grid[i][6:12] for i in range(6, 12)]
    right = [grid[i][12:18] for i in range(6, 12)]
    back = [grid[i][18:24] for i in range(6, 12)]
    bottom = [grid[i][6:12] for i in range(12, 18)]

    # Flatten each face into a single list of 36 elements
    cube = [sum(face, []) for face in [top, left, front, right, back, bottom]]

    return cube

def get_pieces(sides, piece_locations):
    pieces = ""
    for side in sides:
        for piece in piece_locations:
            pieces += side[piece]

    return list(pieces)

def get_outer_x_centers(sides):
    return get_pieces(sides, [7, 10, 28, 25])

def get_inner_x_centers(sides):
    return get_pieces(sides, [14, 15, 21, 20])

def get_clockwise_obliques(sides):
    return get_pieces(sides, [9, 22, 26, 13])

def get_counterclockwise_obliques(sides):
    return get_pieces(sides, [8, 16, 27, 19])

def get_outer_wings(sides):
    return get_pieces(sides, [4, 29, 31, 6])

def get_inner_wings(sides):
    return get_pieces(sides, [3, 23, 32, 12])

def get_corners(sides):
    return get_pieces(sides, [0, 5, 35, 30])

# gets the index of the buffer
def letter_to_number(letter):
    return ord(letter.lower()) - ord('a')

# gets a letter based on an index
def number_to_letter(number):
    number += 1
    if 1 <= number <= 26:
        return chr(ord('a') + number - 1)
    else:
        raise ValueError("Number must be between 1 and 26")

def add_spaces_to_memo(s):
    return ' '.join(s[i:i + 2] for i in range(0, len(s), 2))

# is a piece solved based on its relative index
def color_in_correct_index(color, index):
    if index in [0, 1, 2, 3] and color == "W":
        return True
    if index in [4, 5, 6, 7] and color == "O":
        return True
    if index in [8, 9, 10, 11] and color == "G":
        return True
    if index in [12, 13, 14, 15] and color == "R":
        return True
    if index in [16, 17, 18, 19] and color == "B":
        return True
    if index in [20, 21, 22, 23] and color == "Y":
        return True

    return False

def solve_outer_x_centers(outer_x_centers, buffer):
    memo = ""
    buffer_color = outer_x_centers[buffer]
    memo_finished = False

    while not memo_finished:

        pieces_to_attempt_swap_to = []
        match buffer_color:
            case "W":
                pieces_to_attempt_swap_to = [0, 1, 2, 3]
            case "O":
                pieces_to_attempt_swap_to = [4, 5, 6, 7]
            case "G":
                pieces_to_attempt_swap_to = [8, 9, 10, 11]
            case "R":
                pieces_to_attempt_swap_to = [12, 13, 14, 15]
            case "B":
                pieces_to_attempt_swap_to = [16, 17, 18, 19]
            case "Y":
                pieces_to_attempt_swap_to = [20, 21, 22, 23]

        # check all 4 pieces on the side for an unsolved piece
        for potential_piece_to_swap_to in pieces_to_attempt_swap_to:
            if not outer_x_centers[potential_piece_to_swap_to] == buffer_color:

                # swap the colors of the buffer and the swapping piece
                outer_x_centers[potential_piece_to_swap_to], buffer_color = buffer_color, outer_x_centers[potential_piece_to_swap_to]
                memo += number_to_letter(potential_piece_to_swap_to)
                break

        # all 4 pieces on the side to swap to are already solved. this means it's time for a cycle break!
        else:
            for i, potential_piece_color_to_swap_to in enumerate(outer_x_centers):
                if not color_in_correct_index(potential_piece_color_to_swap_to, i):

                    # swap the colors of the buffer and the swapping piece
                    outer_x_centers[i], buffer_color = buffer_color, outer_x_centers[i]
                    memo += number_to_letter(i)
                    break

            # there are no unsolved pieces - that means the memo is finished!
            else:
                memo_finished = True

    return memo


args = sys.argv[1:]

if len(args) == 0:
    scramble = scrambler666.get_WCA_scramble()
    print("Scramble:")
    print(scramble)
    print()

    cube = magiccube.Cube(6)
    cube.rotate(scramble)

    print()
    print(cube)
    print()

    parsed_cube = cube.get()

    # Reshape into 6 lists of 36
    cube_sides = [parsed_cube[i:i + 36] for i in range(0, 216, 36)]

    print(get_outer_x_centers(cube_sides))
    print(get_inner_x_centers(cube_sides))
    print(get_clockwise_obliques(cube_sides))
    print(get_counterclockwise_obliques(cube_sides))
    print(get_outer_wings(cube_sides))
    print(get_inner_wings(cube_sides))
    print(get_corners(cube_sides))

    outer_x_center_buffer = letter_to_number("a")

    x_center_memo = add_spaces_to_memo(solve_outer_x_centers(get_outer_x_centers(cube_sides), outer_x_center_buffer))
    print(x_center_memo.upper())

    quit()

if args[1] == "-h" or args == "--help":
    print_help()

