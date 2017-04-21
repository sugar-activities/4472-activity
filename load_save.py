#load_save.py
import g

loaded=[] # list of strings

def load(f):
    global loaded
    try:
        for line in f.readlines():
            loaded.append(line)
    except:
        pass

def save(f):
    f.write(str(g.level)+'\n')
    if g.saved_n>0:
        f.write(str(g.saved_n)+'\n')
        for ind in range(g.saved_n):
            lst=g.save[ind]
            f.write(str(len(lst))+'\n')
            for v in lst:
                f.write(str(v)+'\n')

# note need for rstrip() on strings
def retrieve():
    global loaded
    if len(loaded)>0:
        g.level=int(loaded[0])
        if len(loaded)>1:
            g.save=[]
            g.saved_n=int(loaded[1]) # of saved programs
            g.load_n=g.saved_n
            ind=2
            for i in range(g.saved_n):
                n=int(loaded[ind]); ind+=1 # of boxes in this program
                lst=[]
                for j in range(n):
                    lst.append(int(loaded[ind])); ind+=1
                g.save.append(lst)
            g.save_n=g.saved_n+1
                    
            
            
        
