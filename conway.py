#!/usr/bin/python2
import pygame,sys
import conway_backend
from pygame.locals import*

glider = [(0,0),(1,0),(0,1),(2,1),(0,2)]
conway_backend.gameinit(50)

FPS = 10
WINDOWWIDTH=800
WINDOWHEIGHT=640
GAPSIZE = 1
BOARDWIDTH = conway_backend._boardsize
BOARDHEIGHT = BOARDWIDTH

CONTROLHEIGHT = 30 #Height of control button UI
BUTTONGAP = 10
BOXWIDTH = 12
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

BUTTON_LIST = [ (' Start ',start_action),
                (' Stop ',stop_action),
                (' Reset ',reset_action)
              ]
BUTTON_ACTIONS = {} #dict to lookup actions, filled from BUTTON_LIST
BUTTONS=[] #[(name,surfaceobj,rectobj)] list of tuples filled in button_setup from BUTTON_NAMES


def button_setup() :
    global BUTTONS,BUTTON_ACTIONS,BUTTON_LIST
    i=0
    lastwidth=0
    startx = left_top_coords(0,0)[0]
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
    drawBoard(board)
    for b in BUTTONS:
        DISPLAYSURF.blit(b[1],b[2]) #b[1]: surface obj, b[2]: rect obj
    pygame.display.update()


def main():
    #init pygame
    global FPSCLOCK, DISPLAYSURF,PAUSED
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Conway's Game of Life")
    button_setup()
    (mousex,mousey) = (0,0)

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
    (boxx,boxy) = getBoxAtPixel(mousex,mousey)
    if boxx !=None and boxy !=None :
        conway_backend.invert((boxx,boxy))
        return

    button = getButtonAtPixel(mousex,mousey)
    if button != None :
        name = button[0]
        BUTTON_ACTIONS[name]()
    return #or maybe we just clicked nowhere



def left_top_coords(boxx,boxy) :
    #Converts grid coordinates to pixel coordinates
    left = boxx * (BOXWIDTH+GAPSIZE) + XMARGIN
    top  = boxy * (BOXHEIGHT+GAPSIZE) + YMARGIN + CONTROLHEIGHT + GAPSIZE
    return (left,top)


def getButtonAtPixel(x,y) :
    global BUTTONS #list of (name,surfobj,rectobj) tuples
    for b in BUTTONS:
        button_rect = b[2]
        if button_rect.collidepoint(x,y) :
            return b
    return None

def getBoxAtPixel(x,y) :
    for boxx in range(BOARDWIDTH) :
        for boxy in range(BOARDWIDTH) :
            left,top = left_top_coords(boxx,boxy)
            boxRect = pygame.Rect(left,top,BOXWIDTH,BOXHEIGHT)
            if boxRect.collidepoint(x,y) :
                return (boxx,boxy)
    return (None,None)


def drawBoard(board) :
    for boxx in range(BOARDWIDTH) :
        for boxy in range(BOARDHEIGHT) :
            (left,top) = left_top_coords(boxx,boxy)
            currcolor = ALIVECOLOR if (boxx,boxy) in board else DEADCOLOR
            pygame.draw.rect(DISPLAYSURF, currcolor, (left,top,BOXWIDTH,BOXHEIGHT))


if __name__=="__main__" :
    main()

'''
def debugprint():
    print "-- Backend --" 
    print "backend._boardsize",conway_backend._boardsize 
    print "backend._board",conway_backend._board 
    print "-- Graphics --" 
    print "FPS:",FPS 
    print "WINDOWWIDTH:",WINDOWWIDTH 
    print "WINDOWHEIGHT:",WINDOWHEIGHT 
    #print "BOXSIZE:",BOXSIZE 
    print "BOXWIDTH:",BOXWIDTH
    print "BOXHEIGHT:",BOXHEIGHT
    print "GAPSIZE:",GAPSIZE 
    print "BOARDWIDTH:",BOARDWIDTH 
    print "BOARDHEIGHT:",BOARDHEIGHT 
    print "XMARGIN:",XMARGIN 
    print "YMARGIN:",YMARGIN 
    print "ALIVECOLOR:",ALIVECOLOR 
    print "DEADCOLOR:",DEADCOLOR 
    print "BGCOLOR:",BGCOLOR 
'''

