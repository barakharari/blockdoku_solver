from math import sqrt

# Everything is right shifted

# Equal to 10000... top right of grid
GRID = 1208925819614629174706176
SIZE_OF_ROW = SIZE_OF_COLUMN = NUMBER_OF_ROWS = NUMBER_OF_COLUMNS = NUMBER_OF_SQUARES = 9
SQUARES_PER_ROW = SQUARES_PER_COLUMN = COLUMNS_PER_SQUARE = ROWS_PER_SQUARE = int(sqrt(SIZE_OF_ROW))

# Make sure amount of squares = size of row = size of column
# or else assumptions we make later will not apply
assert SQUARES_PER_ROW * SQUARES_PER_ROW == SIZE_OF_ROW

# 100000000_100000000_100000000_1000...
COLUMN_MAP = sum([GRID >> SIZE_OF_ROW*i for i in range(NUMBER_OF_ROWS)])

# 111111111_000000000_000000000_0000...
ROW_MAP = sum([GRID >> i for i in range(SIZE_OF_ROW)])

# 111000000_111000000_111000000_0000...
# Add on the layers of the square based on square size
# We do 'i*SIZE_OF_ROW' gives us the correct row, 'j' gives us correct column
SQUARE_MAP = sum([GRID >> i*SIZE_OF_ROW+j for i in range(SQUARES_PER_ROW) for j in range(SQUARES_PER_ROW)])

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
1: 
   []
1: 
   [][]
1: 
   [][][]
1: 
   [][][][]
1: 
   [][][][][]
2: 
   []
   []
2: 
   []
   []
   []
2: 
   []
   []
   []
   []
2: 
   []
   []
   []
   []
   []
3:
   []
   []
   [][][]
3:
       []
       []
   [][][]
3:
   [][][]
   []
   []
3:
   [][][]
       []
       []
4: 
   [][]
   []
4: 
   [][]
     []
4:
   []
   [][]
4: 
     []
   [][]
5:
   [][][]
   []
5:
   [][][]
       []
5:
   []
   []
   [][]
5:
     []
     []
   [][]
6: 
   []
   [][]
   []
6:
     []
   [][]
     []
6:
   [][][]
     []
6:
     []
   [][][]
7: 
   [][]
   []
   [][]
7:
   [][]
     []
   [][]
7:
   [][][]
   []  []
7:
   []  []
   [][][]
8: 
     []
   [][][]
     []
9:
     []
   []
9:
   []
     []
10:
       []
     []
   []
10:  
   []
     []
       []
'''

# Piece number, width, height
pieces = [

   #1
   [1208925819614629174706176,1,1],
   [1813388729421943762059264,2,1],
   [2115620184325601055735808,3,1],
   [2266735911777429702574080,4,1],
   [2342293775503344025993216,5,1],

   #2
   [1211287002856063997313024,1,2],
   [1211291614542082424700928,1,3],
   [1211291623549281679441920,1,4],
   [1211291623566873865486336,1,5],

   #3
   [2117985979253054305730560,3,3],
   [2116211633057464368234496,3,3],
   [1211295073306596245241856,3,3],
   [302829821164548247257088,3,3],

   #4
   [1212467594476781408616448,2,2],
   [608004684669466821263360,2,2],
   [1815749912663378584666112,2,2],
   [1814569321042661173362688,2,2],

   #5
   [1213057890287140114268160,3,2],
   [306363525576168233238528,3,2],
   [1815754524349397012054016,2,3],
   [1814571626885670387056640,2,3],

   #6
   [1212472206162799836004352,2,3],
   [608006990512476034957312,2,3],
   [608594980479825526915072,3,2],
   [2116800775946318467039232,3,2],

   #7
   [1815756830192406225747968,2,3],
   [1814576238571688814444544,2,3],
   [1515289345190797407944704,3,2],
   [2118571663377394583994368,3,2],

   #8
   [608597286322834740609024,3,3],

   #9
   [1210106411235346586009600,2,2],
   [606824093048749409959936,2,2],

   #10
   [1210107564156851192856576,3,3],
   [303416658210393132367872,3,3]
]

# ZERO_INDEXING
# Return true if row,column activated
def activation(state, row, column):
   shift = row*SIZE_OF_ROW+column
   return (state & (GRID >> shift)) != 0

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

# Return new state if piece first, else return -1
# Caller is responsible for ensuring the piece fits
def check_and_place_piece(state, row, column, piece_num):
   shifted_piece = piece_num >> (row*SIZE_OF_ROW) # move y-axis
   shifted_piece = shifted_piece >> column # move x-axis
   if ((state & shifted_piece) == 0):
      return state + shifted_piece
   return -1

def check_piece(state, row, column, piece_num):
   shifted_piece = piece_num >> (row*SIZE_OF_ROW) # move y-axis
   shifted_piece = shifted_piece >> column # move x-axis
   return (state & shifted_piece) == 0

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

def score_board(state, pieces=pieces):
   score = 0
   for piece in pieces:
      p_num, p_width, p_height = piece
      for row in range(SIZE_OF_ROW-p_width+1):
         for column in range(SIZE_OF_COLUMN-p_height+1):
            score += check_piece(state, row, column, p_num)
   return score

def calculate_next_best_state_reg(state, pieces, row, column, best_state_and_score=[0,0]):

   p_num, p_width, p_height = pieces[0]

   # At the end of grid or no more pieces to fit in
   if (row > SIZE_OF_ROW-p_height):
      return best_state_and_score
   
   # Got past boundary trying to fit piece, move on to next row
   if (column > SIZE_OF_COLUMN-p_width):
      return calculate_next_best_state_reg(state, pieces, row+1, 0, best_state_and_score)
   
   # Try placing piece
   candidate_state = check_and_place_piece(state, row, column, p_num)
   if (candidate_state == -1):
      return calculate_next_best_state_reg(state, pieces, row, column+1, best_state_and_score)

   # Clear any rows/columns/squares
   for i in range(NUMBER_OF_ROWS):
      if(check_row(state, i)):
         candidate_state = clear_row(candidate_state, i)
      if(check_column(state, i)):
         candidate_state = clear_column(candidate_state, i)
      if(check_square(state, i)):
         candidate_state = clear_square(candidate_state, i)

   # Piece can be placed
   if (len(pieces) == 1):
      # Test board once all three pieces have been selected
      candidate_score = score_board(candidate_state)
      if (candidate_score > best_state_and_score[1]):
         best_state_and_score = [candidate_state, candidate_score]
      # Important: pass state in because we aren't solidfying the last piece
      return calculate_next_best_state_reg(state, pieces, row, column+p_width, best_state_and_score) 
   else:
      candidate_state_score = calculate_next_best_state(candidate_state, pieces[1:])
      if (candidate_state_score[1] > best_state_and_score[1]):
         return candidate_state_score
      return best_state_and_score
   
   
def calculate_next_best_state(state, pieces):

   best_state, best_score = 0, 0

   for row in range(SIZE_OF_ROW):
      for column in range(SIZE_OF_COLUMN):
         candidate_state, candidate_score = calculate_next_best_state_reg(state, pieces, row, column)
         if (candidate_score > best_score):
            best_state = candidate_state
            best_score = candidate_score
   
   return [best_state, best_score]

def output_state(state):
   mask = ROW_MAP
   for i in range(NUMBER_OF_ROWS-1, -1, -1):
      output = (state & (mask >> (SIZE_OF_ROW*i))) >> (SIZE_OF_ROW*(NUMBER_OF_ROWS-1-i))
      print(format(output,'0'+str(SIZE_OF_ROW)+'b'))