#!/usr/bin/python
# SimCom.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,sys,buttons,slider,load_save
try:
    import gtk
except:
    pass
import sim

class SimCom:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        if g.help_on:
            if g.help_img==None:
                g.help_img=utils.load_image('help.png')
            g.screen.blit(g.help_img,(0,0))
            return
        g.screen.fill((70,0,70))
        self.sim.draw()
        if not g.running: buttons.clear()
        buttons.draw()
        self.slider.draw()
        if g.load_n>0:
            utils.display_number(g.load_n,self.load_c,g.font1,utils.CYAN)
        utils.display_number(g.save_n,self.save_c,g.font1,utils.ORANGE)

    def do_click(self):
        # load number
        x,y=self.load_c; d=self.load_d
        if utils.mouse_in(x-d,y-d,x+d,y+d):
            g.load_n+=1
            if g.load_n>g.saved_n: g.load_n=1
            return True
        # save number
        x,y=self.save_c; d=self.load_d
        if utils.mouse_in(x-d,y-d,x+d,y+d):
            g.save_n+=1
            if g.save_n>(g.saved_n+1): g.save_n=1
            return True
        if self.sim.in_box(): return True
        # help (printer image)
        if utils.mouse_on_img(self.sim.printer,self.sim.printer_xy):
            g.help_on=True; buttons.off('help'); return
        n=self.sim.n_pad()
        if n==None: return False
        if n=='enter': self.do_key(13); return True
        if n=='back': self.do_key(8); return True
        if len(self.sim.inos)==4: self.sim.inos=self.sim.inos[1:]
        self.sim.inos.append(n)
        return True

    def right_click(self):
        # load number
        x,y=self.load_c; d=self.load_d
        if utils.mouse_in(x-d,y-d,x+d,y+d):
            g.load_n-=1
            if g.load_n<1: g.load_n=g.saved_n
            return True
        # save number
        x,y=self.save_c; d=self.load_d
        if utils.mouse_in(x-d,y-d,x+d,y+d):
            g.save_n-=1
            if g.save_n<1: g.save_n=g.saved_n+1
            return True
        return False
    
    def do_button(self,bu):
        if bu=='green':
            if g.running:
                g.running=False; buttons.clear()
            else:
                buttons.stay_down('green'); g.running=True
        elif bu=='yellow':
            g.running=False; buttons.clear(); self.sim.step()
        elif bu=='cream':
            g.running=False; buttons.clear(); self.sim.clear()
        elif bu=='cyan':
            g.running=False; buttons.clear(); self.sim.clear()
            self.sim.load()
        elif bu=='orange':
            g.running=False; buttons.clear()
            self.sim.save()
            if g.saved_n>0: buttons.on('cyan')
        elif bu=='help':
            g.help_on=True; buttons.off('help'); return

    def do_key(self,key):
        if key in g.CROSS:
            if self.do_click(): return
            if self.slider.mouse(): return
            bu=buttons.check()
            if bu!='': self.do_button(bu)
            return
        if key in g.TICK:
            self.change_level(); self.flush_queue(); return
        if key==pygame.K_v: g.version_display=not g.version_display; return
        if key==13: self.sim.finalise_input(); return
        if key==8:
            if len(self.sim.inos)>0: self.sim.inos.pop()
            return
        if key in g.NUMBERS:
            n=g.NUMBERS[key]
            if len(self.sim.inos)==4: self.sim.inos=self.sim.inos[1:]
            self.sim.inos.append(n)
            return
        if key==pygame.K_p: self.sim.load_primes(); return
        if key in g.DOWN: self.sim.inc_r(); return
        if key in g.UP: self.sim.dec_r(); return
        if key in g.RIGHT: self.sim.inc_c(); return
        if key in g.LEFT: self.sim.dec_c(); return

    def change_level(self):
        g.level+=1
        if g.level>self.slider.steps: g.level=1

    def update(self):
        if g.running:
            if g.level==self.slider.steps: self.sim.step(); return
            d=pygame.time.get_ticks()-g.ms
            if d>(self.slider.steps-g.level)*500: # delay in ms
                self.sim.step(); g.ms=pygame.time.get_ticks()

    def buttons_setup(self):
        cx=g.sx(1.8); cy=g.sy(18.8); dx=g.sy(3.2); dy=g.sy(2)
        buttons.Button('green',(cx,cy)); cx+=dx
        buttons.Button('yellow',(cx,cy)); cx+=dx
        buttons.Button('cream',(cx,cy)); cx+=dx
        buttons.Button('cyan',(cx,cy))
        self.load_c=cx,cy+dy; cx+=dx; self.load_d=g.sy(.5)
        buttons.Button('orange',(cx,cy))
        self.save_c=cx,cy+dy; cx+=dx
        buttons.Button('help',(g.sx(27.77),g.sy(2.8)))

    def flush_queue(self):
        flushing=True
        while flushing:
            flushing=False
            if self.journal:
                while gtk.events_pending(): gtk.main_iteration()
            for event in pygame.event.get(): flushing=True

    def run(self):
        g.init()
        if not self.journal: utils.load()
        self.sim=sim.Sim()
        load_save.retrieve()
        self.buttons_setup()
        if g.saved_n==0: buttons.off('cyan')
        self.slider=slider.Slider(g.sx(23.4),g.sy(20.2),5,utils.GREEN)
        if self.canvas<>None: self.canvas.grab_focus()
        ctrl=False
        pygame.key.set_repeat(600,120); key_ms=pygame.time.get_ticks()
        going=True
        while going:
            if self.journal:
                # Pump GTK messages.
                while gtk.events_pending(): gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos=event.pos
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if g.help_on: g.help_on=False 
                    elif event.button==1:
                        if self.do_click():
                            pass
                        elif self.slider.mouse():
                            pass # level changed
                        else:
                            bu=buttons.check()
                            if bu!='': self.do_button(bu); self.flush_queue()
                    elif event.button==3:
                        self.right_click()
                elif event.type == pygame.KEYDOWN:
                    # throttle keyboard repeat
                    if pygame.time.get_ticks()-key_ms>110:
                        key_ms=pygame.time.get_ticks()
                        if ctrl:
                            if event.key==pygame.K_q:
                                if not self.journal: utils.save()
                                going=False; break
                            else:
                                ctrl=False
                        if event.key in (pygame.K_LCTRL,pygame.K_RCTRL):
                            ctrl=True; break
                        self.do_key(event.key); g.redraw=True
                        self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl=False
            if not going: break
            self.update()
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                g.screen.blit(g.pointer,g.pos)
                pygame.display.flip()
                g.redraw=False
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((1024,768),pygame.FULLSCREEN)
    game=SimCom()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
