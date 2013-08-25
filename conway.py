#!/usr/bin/python2
import pygame,sys
import conway_backend
from pygame.locals import *

glider = [(0,0),(1,0),(0,1),(2,1),(0,2)]
conway_backend.gameinit(50,glider)

FPS = 10
WINDOWWIDTH=800
WINDOWHEIGHT=640
GAPSIZE = 1
BOARDWIDTH = conway_backend._boardsize
BOARDHEIGHT = BOARDWIDTH

BOXWIDTH = 10
BOXHEIGHT = 10
XMARGIN = (WINDOWWIDTH - BOXWIDTH*BOARDWIDTH - (GAPSIZE * (BOARDWIDTH-1))) // 2
YMARGIN = (WINDOWHEIGHT - BOXHEIGHT*BOARDHEIGHT - (GAPSIZE * (BOARDHEIGHT-1))) // 2

ALIVECOLOR = (255,255,255) #white
DEADCOLOR = (60,60,100) #navy
BGCOLOR = (0,0,0) #black

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


def main():
    #init pygame
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Conway's Game of Life")

    while True :
        DISPLAYSURF.fill(BGCOLOR) #Really need this again?
        conway_backend.advance()
        drawBoard(conway_backend._board)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        #Event handler
        for event in pygame.event.get() :
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()


def left_top_coords(boxx,boxy) :
    #Converts grid coordinates to pixel coordinates
    left = boxx * (BOXWIDTH+GAPSIZE) + XMARGIN
    top  = boxy * (BOXHEIGHT+GAPSIZE) + YMARGIN
    return (left,top)


def getBoxAtPixel(x,y) :
    for boxx in range(BOARDWIDTH) :
        for boxy in range(BOARDWIDTH) :
            left,top = left_top_coords(boxx,boxy)
            boxRect = pygame.REct(left,top,BOXWIDTH,BOXHEIGHT)
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
