# g.py - globals
import pygame,utils,random

app='SimCom'; ver='1'
ver='21'
ver='22'
# save number changeable
ver='23'
# right click = # decrease
ver='24'
# help screen
ver='25'
# help & back buttons
ver='26'
# fixed for non-standard displays - sim.py y0=

UP=(264,273)
DOWN=(258,274)
LEFT=(260,276)
RIGHT=(262,275)
CROSS=(259,120)
CIRCLE=(265,111)
SQUARE=(263,32)
TICK=(257,) # 13 removed in SimCom
NUMBERS={pygame.K_1:1,pygame.K_2:2,pygame.K_3:3,pygame.K_4:4,\
           pygame.K_5:5,pygame.K_6:6,pygame.K_7:7,pygame.K_8:8,\
           pygame.K_9:9,pygame.K_0:0}

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,font3,clock
    global factor,offset,imgf,message,version_display
    global pos,pointer
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    clock=pygame.time.Clock()
    if pygame.font:
        t=int(50*imgf); font1=pygame.font.Font(None,t)
        t=int(25*imgf); font2=pygame.font.Font(None,t)
        t=int(42*imgf); font3=pygame.font.Font(None,t)
    message=''
    pos=pygame.mouse.get_pos()
    pointer=utils.load_image('pointer.png',True)
    pygame.mouse.set_visible(False)
    
    # this activity only
    global level,running,ms,save,save_n,load_n,saved_n,help_img,help_on
    level=1 #speed
    running=False
    ms=pygame.time.get_ticks()
    save=[]; save_n=1; load_n=0; saved_n=0
    help_img=None; help_on=False
    
def sx(f): # scale x function
    return int(f*factor+offset+.5)

def sy(f): # scale y function
    return int(f*factor+.5)
