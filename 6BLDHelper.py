import sys
from cubescrambler import scrambler666
import magiccube

piece_list_debugging = True

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
def color_on_correct_side(color, index):
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

def get_piece_list_matrix(piece_list):
    if len(piece_list) != 24:
        raise ValueError("Input list must have exactly 24 elements.")
    return [piece_list[i:i+4] for i in range(0, 24, 4)]


# decide what side to swap the buffer location piece to depending on the color of the piece in the buffer position.
# make sure that the buffer position is not in the list, because we never want to attempt to swap to the buffer.
def get_pieces_to_attempt_swap_to(buffer, buffer_color):
    match buffer_color:
        case "W":
            return [i for i in range(0, 4) if i != buffer]
        case "O":
            return [i for i in range(4, 8) if i != buffer]
        case "G":
            return [i for i in range(8, 12) if i != buffer]
        case "R":
            return [i for i in range(12, 16) if i != buffer]
        case "B":
            return [i for i in range(16, 20) if i != buffer]
        case "Y":
            return [i for i in range(20, 24) if i != buffer]

def solve_center_pieces(piece_list, buffer):
    memo = ""
    memo_finished = False

    piece_list_matrix = []
    if piece_list_debugging: piece_list_matrix = get_piece_list_matrix(piece_list)

    while not memo_finished:

        pieces_to_attempt_swap_to = get_pieces_to_attempt_swap_to(buffer, piece_list[buffer])

        # check all 4 pieces on the side for an unsolved piece
        for potential_piece_to_swap_to in pieces_to_attempt_swap_to:
            if not piece_list[potential_piece_to_swap_to] == piece_list[buffer]:

                # swap the colors of the buffer and the swapping piece
                piece_list[potential_piece_to_swap_to], piece_list[buffer] = piece_list[buffer], piece_list[potential_piece_to_swap_to]

                memo += number_to_letter(potential_piece_to_swap_to)
                break

        # all 4 pieces on the side to swap to are already solved. this means it's time for a cycle break!
        else:
            for i, potential_piece_color_to_swap_to in enumerate(piece_list):
                if i == buffer:
                    continue  # don't try to swap with the buffer itself

                if not color_on_correct_side(potential_piece_color_to_swap_to, i):

                    # swap the colors of the buffer and the swapping piece
                    piece_list[i], piece_list[buffer] = piece_list[buffer], piece_list[i]

                    memo += number_to_letter(i)
                    break

            # there are no unsolved pieces - that means the memo is finished!
            else:
                memo_finished = True

    return memo.upper()

args = sys.argv[1:]

if len(args) == 0:
    #scramble = scrambler666.get_WCA_scramble()
    scramble = "Dw' Rw Fw2 F R 3Uw' Rw2 U Rw2 L F U Uw Bw D2 3Rw' Dw' L' Rw 3Uw' L B R Dw L2 Lw2 U' F' Lw Bw Rw2 3Rw F R2 L Dw2 Lw B2 R 3Rw 3Uw2 3Rw2 L' 3Uw Lw D' F 3Rw2 L2 Dw2 3Uw R' 3Fw' Bw D' R2 Fw' Uw' 3Rw2 U' F2 Rw 3Rw' Lw R2 Uw2 B F Uw2 L' U2 D2 Lw2 F' L R2 Lw 3Fw Dw' Uw"
    print("Scramble:")
    print(scramble)
    print()

    cube = magiccube.Cube(6)
    cube.rotate(scramble)

    parsed_cube = cube.get()

    # Reshape into 6 lists of 36
    cube_sides = [parsed_cube[i:i + 36] for i in range(0, 216, 36)]

    outer_x_centers = get_outer_x_centers(cube_sides)
    inner_x_centers = get_inner_x_centers(cube_sides)
    clockwise_obliques = get_clockwise_obliques(cube_sides)
    counterclockwise_obliques = get_counterclockwise_obliques(cube_sides)
    outer_wings = get_outer_wings(cube_sides)
    inner_wings = get_inner_wings(cube_sides)
    corners = get_corners(cube_sides)

    print(outer_x_centers)
    print(outer_wings)
    print(clockwise_obliques)
    print(counterclockwise_obliques)
    print(outer_wings)
    print(inner_wings)
    print(corners)

    outer_x_center_buffer = letter_to_number("a")
    inner_x_center_buffer = letter_to_number("a")
    clockwise_oblique_buffer = letter_to_number("d")
    counterclockwise_oblique_buffer = letter_to_number("d")
    outer_wings_buffer = letter_to_number("u")
    inner_wings_buffer = letter_to_number("u")
    corner_buffer = letter_to_number("a")

    full_memo = ""

    full_memo += add_spaces_to_memo(solve_center_pieces(outer_x_centers, outer_x_center_buffer)) + "\n"
    full_memo += add_spaces_to_memo(solve_center_pieces(inner_x_centers, inner_x_center_buffer)) + "\n"
    full_memo += add_spaces_to_memo(solve_center_pieces(clockwise_obliques, clockwise_oblique_buffer)) + "\n"
    full_memo += add_spaces_to_memo(solve_center_pieces(counterclockwise_obliques, counterclockwise_oblique_buffer))
    #full_memo += add_spaces_to_memo(solve_pieces(outer_wings, outer_wings_buffer, []))
    #full_memo += add_spaces_to_memo(solve_pieces(inner_wings, inner_wings_buffer))

    print(full_memo)

    quit()

if args[1] == "-h" or args == "--help":
    print_help()

