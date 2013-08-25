from copy import deepcopy
#Points denoted by tuples, board represented by a set
_board=set()
_boardsize = 0

def add(pt) :
    '''Adds a live point to the board. pt expected to be represented as a 2-tuple'''
    _board.add(pt)

def remove(pt) :
    '''Removes a live point from the board. pt expected to be represented as a 2-tuple'''
    _board.discard(pt)


def gameinit(sz) :
    '''Simple size setter: May be changed to initialize starting live cells'''
    global _boardsize
    _boardsize=sz


def is_empty():
    return len(_board) == 0


def clear_board() :
    _board.clear()


'''def get_board() :
    return _board'''


def invert(pt):
    '''Kills a cell if it is alive, or adds a cell to the live list if it's dead.
    Helper function useful for handling user clicks.'''
    global _board
    if not is_valid(pt,_boardsize) :
        raise IndexError('Bad point used in invert(pt)')
    if pt in _board :
        _board.remove(pt)
    else :
        _board.add(pt)


def _neighbors(size,pt) :
    '''Generator for getting neighbors of a point, whether alive or dead'''
    if not is_valid(pt,size) :
        raise IndexError('Bad point called in _neighbors(size,pt)')
    yield ((pt[0]+1) % size, (pt[1]-1) % size)
    yield ((pt[0]+1) % size, (pt[1]  ) % size)
    yield ((pt[0]+1) % size, (pt[1]+1) % size)
    yield ((pt[0]  ) % size, (pt[1]-1) % size)
    yield ((pt[0]  ) % size, (pt[1]+1) % size)
    yield ((pt[0]-1) % size, (pt[1]-1) % size)
    yield ((pt[0]-1) % size, (pt[1]  ) % size)
    yield ((pt[0]-1) % size, (pt[1]+1) % size)
    raise StopIteration

def neighbors(pt):
    '''Partial application of _neighbors(pt)'''
    global _boardsize
    return _neighbors(_boardsize,pt)


def is_valid(pt,size) :
    return pt[0] >=0 and pt[0] < size and pt[1] >=0 and pt[1] < size


def count_alive_neighbors(pt) :
    '''Returns number of live neighbors of a given point.  pt expected to be a 2-tuple.'''
    result=0
    for n in neighbors(pt) :
        if n in _board :
            result += 1
    return result

def count_neigh_update_dead(dead_cands,pt) :
    '''Returns # of live neighbors of a point.  Updates dead_cands so that it contains a list of dead points which may be alive in the next generation.'''
    alive_neighbors=0
    for n in neighbors(pt) :
        if n in _board :
            alive_neighbors += 1
        else :
            dead_cands.add(n)
    return alive_neighbors

def iterate(board) :
    '''Worker function for updating board state.  Returns a new set.'''
    #TODO: Some magic numbers here
    newboard = deepcopy(board)
    dead_cands = set() #Candidate cells for reproduction
    for alivept in _board :
        alive_neighbors = count_neigh_update_dead(dead_cands,alivept)
        if alive_neighbors <2 or alive_neighbors > 3 :
            newboard.remove(alivept)

    for deadpt in dead_cands : #TODO: Find pythonic way of expressing this
        if count_alive_neighbors(deadpt) == 3 :
            newboard.add(deadpt)

    return newboard


def advance() :
    '''Advance the game state by one tick.'''
    global _board
    _board = iterate(_board)

