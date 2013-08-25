#!/usr/bin/python2
import pygame,sys
import conway_backend
from pygame.locals import*

GRIDSIZE = 60

FPS = 15
WINDOWWIDTH=1400
WINDOWHEIGHT=840
GAPSIZE = 1
BOARDWIDTH = GRIDSIZE
BOARDHEIGHT = GRIDSIZE

CONTROLHEIGHT = 25 #Height of control button UI
BUTTONGAP = 8
BOXWIDTH = 10
BOXHEIGHT = 10
XMARGIN = (WINDOWWIDTH - BOXWIDTH*BOARDWIDTH - (GAPSIZE * (BOARDWIDTH-1))) // 2
YMARGIN = (WINDOWHEIGHT - CONTROLHEIGHT - BOXHEIGHT*BOARDHEIGHT - (GAPSIZE * (BOARDHEIGHT-1))) // 2

ALIVECOLOR = (255,255,255) #white
DEADCOLOR = (60,60,100) #navy
BGCOLOR = (0,0,0) #black

PAUSED = True

def start_action() :
    global PAUSED
    PAUSED = False


def stop_action() :
    global PAUSED
    PAUSED = True

def reset_action() :
    global PAUSED
    PAUSED = True
    conway_backend.clear_board()

#Defined BUTTON_LIST so that UI would be presented predictably, instead of just using
#BUTTON_ACTIONS dict
BUTTON_LIST = [ (' Start ',start_action),
                (' Stop ',stop_action),
                (' Reset ',reset_action)
              ]
BUTTON_ACTIONS = {} #dict to lookup actions, filled from BUTTON_LIST
BUTTONS=[] #[(name,surfaceobj,rectobj)] list of tuples filled in button_setup from BUTTON_LIST
           #Used to hold buttons graphics data


def button_setup() :
    global BUTTONS,BUTTON_ACTIONS,BUTTON_LIST
    i=0
    lastwidth=0
    startx = left_top_coords(0,0)[0] #only left coords
    fontObj = pygame.font.Font('freesansbold.ttf',18)
    for n in BUTTON_LIST:
        name=n[0]
        action=n[1]
        txtSurf = fontObj.render(name,True,ALIVECOLOR,DEADCOLOR)
        Rect = txtSurf.get_rect()
        Rect.topleft = (startx + lastwidth + i*BUTTONGAP,YMARGIN)
        i += 1
        lastwidth += Rect.width
        BUTTONS.append((name,txtSurf,Rect))
        BUTTON_ACTIONS[name] = action


def draw_all(board) :
    global BUTTONS
    DISPLAYSURF.fill(BGCOLOR)
    draw_board(board)
    for b in BUTTONS:
        DISPLAYSURF.blit(b[1],b[2]) #b[1]: surface obj, b[2]: rect obj
    pygame.display.update()


def main():
    #init pygame
    global FPSCLOCK, DISPLAYSURF, PAUSED
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Conway's Game of Life")
    button_setup()
    (mousex,mousey) = (0,0)
    conway_backend.gameinit(GRIDSIZE)

    while True :
        if not PAUSED :
            conway_backend.advance()
            if conway_backend.is_empty() :
                PAUSED = True
        FPSCLOCK.tick(FPS)
        draw_all(conway_backend._board)
        #Event handler
        for event in pygame.event.get() :
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP :
                (mousex,mousey)=event.pos
                dispatch_click(mousex,mousey)


def dispatch_click(mousex,mousey) :
    (gridx,gridy) = get_box_at_pixel(mousex,mousey)
    if gridx !=None and gridy !=None :
        conway_backend.invert((gridx,gridy))
        return

    button = get_button_at_pixel(mousex,mousey)
    if button != None :
        name = button[0]
        BUTTON_ACTIONS[name]()


def left_top_coords(gridx,gridy) :
    #Converts grid coordinates to pixel coordinates
    left = gridx * (BOXWIDTH+GAPSIZE) + XMARGIN
    top  = gridy * (BOXHEIGHT+GAPSIZE) + YMARGIN + CONTROLHEIGHT + GAPSIZE
    return (left,top)


def get_button_at_pixel(x,y) :
    global BUTTONS #list of (name,surfobj,rectobj) tuples
    for b in BUTTONS:
        button_rect = b[2]
        if button_rect.collidepoint(x,y) :
            return b
    return None

def get_box_at_pixel(x,y) :
    for gridx in range(BOARDWIDTH) :
        for gridy in range(BOARDHEIGHT) :
            left,top = left_top_coords(gridx,gridy)
            box_rect = pygame.Rect(left,top,BOXWIDTH,BOXHEIGHT)
            if box_rect.collidepoint(x,y) :
                return (gridx,gridy)
    return (None,None)


def draw_board(board) :
    for gridx in range(BOARDWIDTH) :
        for gridy in range(BOARDHEIGHT) :
            (left,top) = left_top_coords(gridx,gridy)
            currcolor = ALIVECOLOR if (gridx,gridy) in board else DEADCOLOR
            pygame.draw.rect(DISPLAYSURF, currcolor, (left,top,BOXWIDTH,BOXHEIGHT))


if __name__=="__main__" :
    main()
