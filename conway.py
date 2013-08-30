#!/usr/bin/python2
import pygame,sys
import conway_backend
from pygame.locals import*

''' Global game parameters '''

GRIDSIZE = 60 #Number of cells in one side of the board
PAUSED = True

''' Global Window size parameters '''

FPS = 15
WINDOWWIDTH=1000
WINDOWHEIGHT=840
GAPSIZE = 1 #Number of pixels to display in between cells

CONTROLHEIGHT = 25 #Height of control button UI
BUTTONGAP = 8
BOXWIDTH = 10
BOXHEIGHT = 10
XMARGIN = (WINDOWWIDTH - BOXWIDTH*GRIDSIZE - (GAPSIZE * (GRIDSIZE-1))) // 2
YMARGIN = (WINDOWHEIGHT - CONTROLHEIGHT - BOXHEIGHT*GRIDSIZE - (GAPSIZE * (GRIDSIZE-1))) // 2

''' Global font and color parameters '''

ALIVECOLOR = (255,255,255) #white
DEADCOLOR = (60,60,100) #navy
BGCOLOR = (0,0,0) #black
FONTNAME = 'freesansbold.ttf'
FONTSIZE = 18
CAPTION = "Conway's Game of Life"


def main():
    '''Main game loop. Initializes pygame and board with appropriate parameters.'''
    global DISPLAYSURF, PAUSED 
    pygame.init()
    button_setup()
    board = conway_backend.lifeboard(GRIDSIZE)

    fps_clock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption(CAPTION)
    (mousex,mousey) = (0,0)
    FONT = pygame.font.Font('freesansbold.ttf',18)

    while True :
        if not PAUSED :
            board.iterate()
            if board.is_dead() :
                PAUSED = True
        fps_clock.tick(FPS)
        draw_all(board)
        #Event handler
        for event in pygame.event.get() :
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP :
                (mousex,mousey)=event.pos
                dispatch_click(mousex,mousey,board)


def draw_all(board) :
    '''Draws all game elements: Currently user control buttons, game board.
    Soon: Data like generation number and population'''
    DISPLAYSURF.fill(BGCOLOR)
    draw_board(board)
    draw_buttons()
    draw_info(board.get_population(),board.get_generation())
    pygame.display.update()


def draw_info(population,generation) :
    '''Draws info blobs.  TODO: modify for extensibility'''
    fontobj = pygame.font.Font(FONTNAME,FONTSIZE)
    popsurf = fontobj.render('Population: %s' % (population), True, ALIVECOLOR,DEADCOLOR)
    poprect = popsurf.get_rect()
    poprect.topright = (WINDOWWIDTH - XMARGIN, YMARGIN)

    gensurf = fontobj.render('Generation: %s' % (generation), True, ALIVECOLOR,DEADCOLOR)
    genrect = gensurf.get_rect()
    genrect.topright = (poprect.left - BUTTONGAP, YMARGIN)

    DISPLAYSURF.blit(popsurf,poprect)
    DISPLAYSURF.blit(gensurf,genrect)


def dispatch_click(mousex,mousey,board) :
    '''Handle click events'''
    (gridx,gridy) = get_box_at_pixel(mousex,mousey,board)
    if gridx !=None and gridy !=None :
        board.invert((gridx,gridy))
        return

    button = get_button_at_pixel(mousex,mousey)
    if button != None :
        name = button[0]
        BUTTON_ACTIONS[name](board)


def left_top_coords(gridx,gridy) :
    '''Convert grid coordinates to pixel coordinates'''
    #Converts grid coordinates to pixel coordinates
    left = gridx * (BOXWIDTH+GAPSIZE) + XMARGIN
    top  = gridy * (BOXHEIGHT+GAPSIZE) + YMARGIN + CONTROLHEIGHT + GAPSIZE
    return (left,top)


def get_button_at_pixel(x,y) :
    '''Returns the element of BUTTONS_GRAPHICS that is at pixel coord (x,y)
    or returns None'''
    global BUTTONS_GRAPHICS #list of (name,surf_obj,rect_obj) tuples
    for b in BUTTONS_GRAPHICS:
        button_rect = b[2]
        if button_rect.collidepoint(x,y) :
            return b
    return None


def get_box_at_pixel(x,y,board) :
    '''Returns the grid coordinates of the cell at pixel coordinates (x,y)'''
    #TODO:Can probably improve this, but brief profiling says we don't spend much time here
    for gridx in range(board.get_width()) :
        for gridy in range(board.get_height()) :
            left,top = left_top_coords(gridx,gridy)
            box_rect = pygame.Rect(left,top,BOXWIDTH,BOXHEIGHT)
            if box_rect.collidepoint(x,y) :
                return (gridx,gridy)
    return (None,None)


def draw_board(board) :
    '''Expects a container of alive cells in board that supports "in"'''
    for gridx in range(board.get_width()) :
        for gridy in range(board.get_height()) :
            (left,top) = left_top_coords(gridx,gridy)
            currcolor = ALIVECOLOR if (gridx,gridy) in board.alive_cells() else DEADCOLOR
            pygame.draw.rect(DISPLAYSURF, currcolor, (left,top,BOXWIDTH,BOXHEIGHT))


######### BUTTON FUNCTIONS #########
#TODO: Split this into separate module?
#May make more sense to factor into button classes where each button stores its own action

'''TODO: At the moment, actions must be passed the same set of arguments. TODO
Could solve this with global board, but obviously that's not ideal
Real issue is calling button actions cleanly in dispatch click : can make a big switch on button name to handle arguments, but this works too for now
#For now though, I do like the easy extensibility of buttons and BUTTON_LIST
'''

def button_setup() :
    '''Fills BUTTON_ACTIONS dict and BUTTONS_GRAPHICS list from BUTTON_LIST :
    Automatically spaces buttons based on BUTTONGAP and position of other buttons'''
    global BUTTONS_GRAPHICS,BUTTON_ACTIONS,BUTTON_LIST
    i=0
    lastwidth=0
    startx = left_top_coords(0,0)[0] #only left coords
    for n in BUTTON_LIST:
        name=n[0]
        action=n[1]
        fontobj = pygame.font.Font(FONTNAME,FONTSIZE)
        txtSurf = fontobj.render(name,True,ALIVECOLOR,DEADCOLOR)
        Rect = txtSurf.get_rect()
        Rect.topleft = (startx + lastwidth + i*BUTTONGAP,YMARGIN)
        i += 1
        lastwidth += Rect.width
        BUTTONS_GRAPHICS.append((name,txtSurf,Rect))
        BUTTON_ACTIONS[name] = action


def start_action(board) :
    '''Function called on start button click'''
    global PAUSED
    PAUSED = False


def pause_action(board) :
    '''Function called on stop button click'''
    global PAUSED
    PAUSED = True


def reset_action(board) :
    '''Function called on reset button click'''
    global PAUSED
    PAUSED = True
    board.clear_board()


def quit_action(board) :
    sys.exit()

'''Defined BUTTON_LIST so that UI would be presented predictably, instead of just using
BUTTON_ACTIONS dict which results in unordered buttons in UI.
'''
BUTTON_LIST = [ (' Start ',start_action),
                (' Pause ',pause_action),
                (' Reset ',reset_action),
                (' Quit ',quit_action)
              ]
BUTTON_ACTIONS = {} #dict to lookup actions, filled from BUTTON_LIST
BUTTONS_GRAPHICS = [] #[(name,surfaceobj,rectobj)] list of tuples filled in button_setup from BUTTON_LIST


def draw_buttons() :
    '''Simply displays buttons.'''
    for b in BUTTONS_GRAPHICS:
        DISPLAYSURF.blit(b[1],b[2]) #b[1]: surface obj, b[2]: rect obj


if __name__=="__main__" :
    main()
