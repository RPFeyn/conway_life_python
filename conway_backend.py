from copy import deepcopy
import warnings
#Points denoted by tuples, board represented by a set

class lifeboard(object) :
    def __init__(self,sz = 0) :
        '''Simple size setter: May be changed to initialize starting live cells'''
        self._size=sz
        self._board=set()
        self._generation = 0


    def get_size(self) :
        return self._size

    '''For now, only square boards with toroidal boundary conditions are supported'''
    def get_width(self) : 
        return self._size


    def get_height(self): 
        return self._size


    def get_generation(self) :
        return self._generation


    def alive_cells(self) :
        '''Returns set of alive cells.'''
        return self._board


    def iterate(self) :
        '''Advances the board one generation.'''
        #TODO: Some magic numbers encoding the game of life rules here
        newboard = deepcopy(self._board)
        dead_cands = set() #Candidate cells for reproduction

        for alivept in self._board :
            alive_neighbors = self._count_neigh_update_dead(dead_cands,alivept)
            if alive_neighbors <2 or alive_neighbors > 3 :
                newboard.remove(alivept)

        for deadpt in dead_cands : #TODO: Find pythonic way of expressing this
            if self._count_alive_neighbors(deadpt) == 3 :
                newboard.add(deadpt)

        self._board=newboard
        self._generation += 1


    def add(self,pt) :
        '''Adds a live point to the board. pt expected to be represented as a 2-tuple'''
        if self._is_valid_point(pt) :
            self._board.add(pt)
        else :
            pt = self._convert_to_valid(pt)
            warnings.warn("Warning: lifeboard.add(self,pt) called with invalid point, converted to valid coords")
            

    def remove(self,pt) :
        '''Removes a live point from the board. pt expected to be represented as a 2-tuple'''
        self._board.discard(pt)


    def get_population(self) :
        return len(self._board)


    def is_dead(self):
        '''Returns true if there are 0 live cells'''
        return len(self._board) == 0



    def clear_board(self) :
        self._board.clear()
        self._generation = 0


    def invert(self,pt):
        '''Kills a cell if it is alive, or adds a cell to the live list if it's dead.
        Intended for handling user clicks.'''
        if not self._is_valid_point(pt) :
            pt = self._convert_to_valid(pt)
            warnings.warn("Warning: lifeboard.invert(self,pt) called with bad point, converted to valid coords")

        if pt in self._board :
            self._board.remove(pt)
        else :
            self._board.add(pt)


    def _neighbors(self,pt) :
        '''Generator for getting neighbors of a point, whether alive or dead'''
        if not self._is_valid_point(pt) :
            raise IndexError('Bad point called in _neighbors(size,pt)')
        yield ((pt[0]+1) % self._size, (pt[1]-1) % self._size)
        yield ((pt[0]+1) % self._size, (pt[1]  ) % self._size)
        yield ((pt[0]+1) % self._size, (pt[1]+1) % self._size)
        yield ((pt[0]  ) % self._size, (pt[1]-1) % self._size)
        yield ((pt[0]  ) % self._size, (pt[1]+1) % self._size)
        yield ((pt[0]-1) % self._size, (pt[1]-1) % self._size)
        yield ((pt[0]-1) % self._size, (pt[1]  ) % self._size)
        yield ((pt[0]-1) % self._size, (pt[1]+1) % self._size)
        raise StopIteration


    def _is_valid_point(self,pt) :
        return pt[0] >=0 and pt[0] < self._size and pt[1] >=0 and pt[1] < self._size

    def _convert_to_valid(self,pt) :
        newpt = pt
        for xi in newpt :
            xi %= self._size
        return newpt


    def _count_alive_neighbors(self,pt) :
        '''Returns number of live neighbors of a given point.  pt expected to be a 2-tuple.'''
        result=0
        for n in self._neighbors(pt) :
            if n in self._board :
                result += 1
        return result

    def _count_neigh_update_dead(self,dead_cands,pt) :
        '''Returns # of live neighbors of a point.  Updates dead_cands so that it contains a list of dead points which may be alive in the next generation.'''
        alive_neighbors=0
        for n in self._neighbors(pt) :
            if n in self._board :
                alive_neighbors += 1
            else :
                dead_cands.add(n)
        return alive_neighbors




    
