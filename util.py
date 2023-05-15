from math import sqrt

# Everything is right shifted

# Equal to 10000... top right of grid
GRID = 1208925819614629174706176
SIZE_OF_ROW = SIZE_OF_COLUMN = NUMBER_OF_ROWS = NUMBER_OF_COLUMNS = 9
SQUARES_PER_ROW = SQUARES_PER_COLUMN = COLUMNS_PER_SQUARE = ROWS_PER_SQUARE = int(sqrt(SIZE_OF_ROW))

# Make sure amount of squares = size of row = size of column
# or else assumptions we make later will not apply
assert SQUARES_PER_ROW * SQUARES_PER_ROW == SIZE_OF_ROW

# 100000000_100000000_100000000_1000...
COLUMN_MAP = sum([GRID >> SIZE_OF_ROW*i for i in range(1,NUMBER_OF_ROWS)])

# 111111111_000000000_000000000_0000...
ROW_MAP = sum([GRID >> i for i in range(1,SIZE_OF_ROW)])

# 111000000_111000000_111000000_0000...
# 1) Add on the first rows bottom border of square
SQUARE_MAP = sum([GRID >> i for i in range(1,SQUARES_PER_ROW)]) 
# 2) Add on the rest of the layers of the square based on square size
# We do 'i*SIZE_OF_ROW' gives us the correct row, 'j' gives us correct column
SQUARE_MAP += sum([GRID >> i*SIZE_OF_ROW+j for i in range(1,NUMBER_OF_ROWS) for j in range(SQUARES_PER_ROW)])

'''
ROWS and COLUMNS and SQUARES are ZERO-indexed 
(row 0-8, column 0-8, square 0-8)

Our board is represented as:

        00000000z
        000000000
        000000000
        000000000
        000000000
        000000000
        000000000
        y00000000
        w0000000x

Where state = w000000x_y00000000_000..._0000000z
MSB = bottom left
LSB = top right

We index the board from bottom left to top right as well,
so the position of 'y' would be row=1 column=0
'''

'''
: 
   []
: 
   [][]
: 
   [][][]
: 
   [][][][]
: 
   [][][][][]
: 
   []
   []
: 
   []
   []
   []
: 
   []
   []
   []
   []
: 
   []
   []
   []
   []
   []
: 
   [][]
   []
: 
   [][]
     []
:
   []
   [][]
: 
     []
   [][]
:
   [][][]
   []
:
   [][][]
       []
:
   []
   []
   [][]
:
     []
     []
   [][]
: 
   []
   [][]
   []
:
     []
   [][]
     []
:
   [][][]
     []
:
     []
   [][][]
: 
   [][]
   []
   [][]
:
   [][]
     []
   [][]
:
   [][][]
   []  []
:
   []  []
   [][][]
: 
     []
   [][][]
     []
:
     []
   []
:
   []
     []
:
       []
     []
   []
:  
   []
     []
       []
'''

piece_map = [
    1208925819614629174706176,
    1813388729421943762059264,
    2115620184325601055735808,
    2266735911777429702574080,
    2342293775503344025993216,

    1211287002856063997313024,
    1211291614542082424700928,
    1211291623549281679441920,
    1211291623566873865486336,

    1212467594476781408616448,
    608004684669466821263360,
    1815749912663378584666112,
    1814569321042661173362688,

    1213057890287140114268160,
    306363525576168233238528,
    1815754524349397012054016,
    1814571626885670387056640,

    1212472206162799836004352,
    608006990512476034957312,
    608594980479825526915072,
    2116800775946318467039232,

    1815756830192406225747968,
    1814576238571688814444544,
    1515289345190797407944704,
    2118571663377394583994368,

    608597286322834740609024,

    1210106411235346586009600,
    606824093048749409959936,

    1210107564156851192856576,
    303416658210393132367872 
]

def get_piece(id):
    return piece_map[id]

# ZERO_INDEXING
# Return true if row,column activated
def activation(state, row, column):
    shift = row*SIZE_OF_ROW+column
    return (state & (GRID >> shift)) == 1

# Return true if column full
# Isolating the column bits should return us the column bits
def check_column(state, column):
    expectation = (COLUMN_MAP >> column)
    return (state & expectation) == expectation

# Return true if row full
# Isolating the row bits should return us the row bits
def check_row(state, row):
    expectation = (ROW_MAP >> (row * SIZE_OF_ROW))
    return (state & expectation) == expectation

# Return true if square full
def check_square(state, square):
    shift = square // SQUARES_PER_ROW
    leftover = square % SQUARES_PER_ROW

    expectation = SQUARE_MAP
    
    # shift square on y-axis
    expectation = expectation >> (SIZE_OF_ROW * ROWS_PER_SQUARE * shift)
    # shift square on x-axis
    expectation = expectation >> (SQUARES_PER_ROW * leftover)
    return (state & expectation) == expectation

def clear_column(state, column):
    mask = ~(COLUMN_MAP >> column)
    return state & mask 

def clear_row(state, row):
    mask = ~(ROW_MAP >> (row * SIZE_OF_ROW))
    return state & mask

def clear_square(state, square):
    shift = square // SQUARES_PER_ROW
    leftover = square % SQUARES_PER_ROW

    mask = SQUARE_MAP
    
    # shift square on y-axis
    mask = mask >> (SIZE_OF_ROW * ROWS_PER_SQUARE * shift)
    # shift square on x-axis
    mask = mask >> (SQUARES_PER_ROW * leftover)
    # flip bits
    mask = ~mask
    return state & mask

def score_board(state):
    pass

def calculate_next_moves(state, pieces):
    pass

# This should be a matrix multiplication
def attempt_place_piece(state, piece):
    pass