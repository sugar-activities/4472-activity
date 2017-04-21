# sim.py
import g,pygame,utils,random,os

memory=[]
nos_imgs=[]

class Box:
    def __init__(self,r,c,x,y):
        self.ind=len(memory)
        self.r=r; self.c=c; self.x=x; self.y=y
        self.value=0 # 0...9999
        self.minus=False

class Sim:
    def __init__(self):
        # boxes
        x0=g.sx(.5); y0=g.sy(.5); dx=g.sy(2.35); dy=g.sy(1.65)
        y=y0
        for r in range(10):
            x=x0
            for c in range(10):
                box=Box(r,c,x,y); memory.append(box)
                x+=dx
            y+=dy
        self.rect_w=dx+1; self.rect_h=dy+1
        x-=dx; y+=g.sy(.5); self.ac_xy=x,y
        self.memory_rect=pygame.Rect(x0,y0,10*dx,10*dy)
        self.rect_t1=int(g.sy(.05)+.5); self.rect_t2=int(g.sy(.2)+.5)
        self.address_offset=g.sy(.1); self.dx2=dx/2; self.dy2=dy/2+g.sy(.27)
        # variables
        self.pc=0; self.ac=0; self.output=0; self.minus=False
        self.rts=[]
        # printer
        self.printer=utils.load_image('printer.png',True)
        self.nos=[None,None,None,None,None,None]
        self.printer_xy=g.sx(24.2),g.sy(0)
        self.nos_x=self.printer_xy[0]+g.sy(1.8)
        self.nos_y=g.sy(0.05); self.nos_dy=g.sy(.88)
        # number pad
        self.numbers=utils.load_image('numbers.png',True)
        self.numbers_xy=g.sx(24.8),g.sy(7.8)
        for ind in range(10):
            img=utils.load_image(str(ind)+'.png',True); nos_imgs.append(img)
        self.inos=[]
        self.inos_x=self.numbers_xy[0]+g.sy(1.2)
        self.inos_y=g.sy(8.64); self.inos_dx=g.sy(1.1)
        self.bright=utils.load_image('bright.png',True)
        x,y=self.numbers_xy; x+=g.sy(.65); y+=g.sy(.66); self.bright_xy=x,y
        x,y=self.numbers_xy; x+=g.sy(.8); y+=g.sy(2.85); self.n_xy=x,y
        self.n_dx=g.sy(1.95); self.n_dy=g.sy(1.6)
        #
        self.clear()
    
    def draw(self):
        # memory
        pygame.draw.rect(g.screen,utils.BLACK,self.memory_rect)
        for box in memory:
            rect=pygame.Rect(box.x,box.y,self.rect_w,self.rect_h)
            pygame.draw.rect(g.screen,utils.BLUE,rect,self.rect_t1)
            addr=str(box.ind)
            if box.ind<10: addr='0'+addr
            x=box.x+self.address_offset; y=box.y+self.address_offset
            utils.text_blit1(g.screen,addr,g.font2,(x,y),utils.WHITE)
            value=str(box.value)
            x=box.x+self.dx2; y=box.y+self.dy2
            utils.text_blit(g.screen,value,g.font3,(x,y),utils.WHITE)
        # program counter
        box=memory[self.pc]
        rect=pygame.Rect(box.x,box.y,self.rect_w,self.rect_h)
        pygame.draw.rect(g.screen,utils.YELLOW,rect,self.rect_t2)
        # AC
        rect=pygame.Rect(self.ac_xy,(self.rect_w,self.rect_h))
        pygame.draw.rect(g.screen,utils.BLACK,rect)
        pygame.draw.rect(g.screen,utils.RED,rect,self.rect_t2)
        x,y=self.ac_xy; x+=self.address_offset; y+=self.address_offset
        utils.text_blit1(g.screen,'AC',g.font2,(x,y),utils.WHITE)
        x,y=self.ac_xy; x+=self.dx2; y+=self.dy2
        utils.text_blit(g.screen,str(self.ac),g.font3,(x,y),utils.WHITE)
        # printer
        g.screen.blit(self.printer,self.printer_xy)
        x=self.nos_x; y=self.nos_y
        for n in self.nos:
            if n<>None: utils.display_number1(n,(x,y),g.font3)
            y+=self.nos_dy
        # input
        g.screen.blit(self.numbers,self.numbers_xy)
        if self.input_required: g.screen.blit(self.bright,self.bright_xy)      
        x=self.inos_x; y=self.inos_y
        for n in self.inos:
            g.screen.blit(nos_imgs[n],(x,y)); x+=self.inos_dx

    def clear(self):
        self.pc=0; self.ac=0; self.output=0
        for box in memory: box.value=0; box.minus=False
        self.nos=[None,None,None,None,None,None] # printer
        self.clear_input()
        g.running=False

    def clear_input(self):
        self.inos=[]; self.input_required=None

    def step(self):
        g.redraw=True
        value=memory[self.pc].value
        if value in (0,2,3,5,6): self.proc1(value); return
        if value<100: g.running=False; return # illegal
        s=str(value); p=2
        if len(s)==3: p=1
        op=int(s[:p]); addr=int(s[p:])
        if op<14: self.proc2(op,addr); return
        g.running=False; return # illegal

    def proc1(self,op):
        if op==0: self.clear_input(); g.running=False; return
        if op==2:
            if self.rts==[]: self.clear_input(); g.running=False; return
            self.pc=self.rts.pop(); return
        if op==3:
            if self.pc<99:
                self.inc_pc(); self.ac=memory[self.pc].value; self.inc_pc()
            return
        if op==5:
            if self.pc<99:
                self.inc_pc(); self.ac+=memory[self.pc].value; self.inc_pc()
            self.check_ac()
            return
        if op==6:
            if self.pc<99:
                self.inc_pc(); self.ac-=memory[self.pc].value; self.inc_pc()
            self.check_ac()
            return

    def proc2(self,op,addr):
        if op==1: self.input_required=addr; return
        if op==2: self.print_num(memory[addr].value); self.inc_pc(); return
        if op==3:
            self.ac=memory[addr].value; self.minus=memory[addr].minus
            self.inc_pc(); return
        if op==4: memory[addr].value=self.ac; self.inc_pc(); return
        if op==5:
            self.ac+=memory[addr].value; self.check_ac(); self.inc_pc()
            return
        if op==6:
            self.ac-=memory[addr].value; self.check_ac(); self.inc_pc()
            return
        if op==7: self.pc=addr; return
        if op==8:
            if self.pc<99: self.rts.append(self.pc+1)
            self.pc=addr; return
        if op==9:
            if self.minus: self.pc=addr
            else: self.inc_pc()
            return
        if op==10:
            if self.ac==0: self.pc=addr
            else: self.inc_pc()
            return
        if op==11:
            if self.minus or self.ac==0: self.inc_pc()
            else: self.pc=addr
            return
        if op==12:
            memory[addr].value+=1; self.check_addr(addr); self.inc_pc()
            return
        if op==13:
            memory[addr].value-=1; self.check_addr(addr); self.inc_pc()
            return

    def print_num(self,n):
        if len(self.nos)==6: self.nos=self.nos[1:]
        self.nos.append(n)
        
    def finalise_input(self):
        v=0
        for n in self.inos: v=10*v+n
        addr=self.pc
        if self.input_required!=None: addr=self.input_required
        memory[addr].value=v
        self.input_required=None; self.inos=[]
        self.inc_pc()
        
    def check_addr(self,addr):
        v=memory[addr].value; memory[addr].minus=False
        if v>9999: v-=10000
        if v<0: v+=10000; memory[addr].minus=True
        memory[addr].value=v
    
    def check_ac(self):
        self.minus=False
        if self.ac>9999: self.ac-=10000; return
        if self.ac<0: self.ac+=10000; self.minus=True
        return
    
    def inc_pc(self):
        if self.pc==99: g.running=False; return
        self.pc+=1

    def in_box(self):
        for box in memory:
            if utils.mouse_in(box.x,box.y,box.x+self.rect_w,box.y+self.rect_h):
                self.pc=box.ind; self.clear_input()
                return True
        return False

    def n_pad(self):
        x0,y0=self.n_xy; y=y0; ind=0
        for r in range(4):
            x=x0
            for c in range(3):
                if utils.mouse_in(x,y,x+self.n_dx,y+self.n_dy):
                    return (7,8,9,4,5,6,1,2,3,0,'back','enter')[ind]
                x+=self.n_dx; ind+=1
            y+=self.n_dy
        return None
        
    def inc_r(self):
        self.pc+=10
        if self.pc>99: self.pc-=100
        
    def dec_r(self):
        self.pc-=10
        if self.pc<0: self.pc+=100

    def inc_c(self):
        c=memory[self.pc].c
        self.pc+=1
        if c==9: self.pc-=10
        
    def dec_c(self):
        c=memory[self.pc].c
        self.pc-=1
        if c==0: self.pc+=10
        
    def load(self):
        ind=g.load_n-1
        lst=g.save[ind]
        ind=0
        for v in lst: memory[ind].value=v; ind+=1

    def save(self):
        empty=True
        for i in range(100):
            ind=99-i
            if memory[ind].value!=0: empty=False; break
        if empty: return # nothing to save
        lst=[]
        for i in range(ind+1): lst.append(memory[i].value)
        if g.save_n>g.saved_n:
            g.save.append(lst); g.saved_n+=1
            g.load_n=g.saved_n; g.save_n+=1
        else:
            g.save[g.save_n-1]=lst

    def load_primes(self):
        self.clear()
        fname=os.path.join('data','primes.txt')
        f=open(fname, 'r')
        for ind in range(51):
            v=int(f.readline()); memory[ind].value=v
        f.close()


        
        
            
            
        
        
