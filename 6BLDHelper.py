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

    return pieces

def get_outer_x_centers(sides):
    return get_pieces(sides, [7, 10, 28, 25])

def get_inner_x_centers(sides):
    return get_pieces(sides, [14, 15, 21, 20])

def get_clockwise_obliques(sides):
    return get_pieces(sides, [9, 22, 26, 13])

def get_counterclockwise_obliques(sides):
    return get_pieces(sides, [8, 16, 27, 19])

# gets the index of the buffer
def letter_to_number(letter):
    return ord(letter.lower()) - ord('a')

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

    buffer = letter_to_number("a")

    quit()

if args[1] == "-h" or args == "--help":
    print_help()

