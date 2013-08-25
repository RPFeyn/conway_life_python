from copy import deepcopy
#Points denoted by tuples, board represented by a set
_board=set()
_boardsize = 0


def add(pt) :
    _board.add(pt)


def remove(pt) :
    _board.discard(pt)


def gameinit(sz) :
    global _boardsize
    global _board
    _boardsize=sz


def is_empty():
    return len(_board) == 0


def clear_board() :
    _board.clear()


def get_board() :
    return _board

def invert(pt):
    global _board
    if not is_valid(pt,_boardsize) :
        raise IndexError('Bad point used in invert(pt)')
    if pt in _board :
        _board.remove(pt)
    else :
        _board.add(pt)


def _neighbors(size,pt) :
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
    global _boardsize
    return _neighbors(_boardsize,pt)


def is_valid(pt,size) :
    return pt[0] >=0 and pt[0] < size and pt[1] >=0 and pt[1] < size


def count_alive_neighbors(pt) :
    result=0
    for n in neighbors(pt) :
        if n in _board :
            result += 1
    return result

def count_neigh_update_dead(dead_cands,pt) :
    alive_neighbors=0
    for n in neighbors(pt) :
        if n in _board :
            alive_neighbors += 1
        else :
            dead_cands.add(n)
    return alive_neighbors

def iterate(board) :
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
    global _board
    _board = iterate(_board)

