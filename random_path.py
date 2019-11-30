__author__ = 'Булыгина Настя bulygina07@yandex.ru'

from tkinter import *
import random


class P():
    def __init__(self, root, color, node, target, maps, ban):
        self.root = root
        self.color = color
        self.y = node[0]
        self.x = node[1]
        P.target = target
        self.count = 0
        
        self.visit = {}
        P.hierarchy = {}
        P.neighbor = {}
        
        self.init_3_dict(maps, ban)
        
    def init_3_dict(self, maps, ban):
        def is_en(yx):
            if yx[0] < 0 or yx[0] > len(maps)-1: return
            if yx[1] < 0 or yx[1] > len(maps[0])-1: return
            if yx in ban: return
            return True
        
        for y in range(len(maps)):
            for x in range(len(maps[0])):
                self.visit[(y,x)] = 0
                P.hierarchy[(y,x)] = maps[y][x]
                
                n = []
                if is_en((y-1,x)):
                    n.append((y-1,x))
                if is_en((y+1,x)):
                    n.append((y+1,x))
                if is_en((y,x-1)):
                    n.append((y,x-1))
                if is_en((y,x+1)):
                    n.append((y,x+1))
                    
                P.neighbor[(y,x)] = n
        
        
    def show(self, y, x, color):
        lb = Label(text=" ", background = color)
        lb.configure(text=P.hierarchy[(y,x)] )
        lb.grid(row=self.y, column=self.x, ipadx=10, ipady=5, padx=1, pady=1)
        
             
    def move(self):
        v = []
        for i in P.neighbor[(self.y, self.x)]:
            v.append(i)    
        y,x = random.choice(v)
        
        self.show(self.y, self.x, 'white')    
        self.y = y
        self.x = x
        self.show(y, x, self.color)
        
        self.count +=1
        
        if P.target == P.hierarchy[(self.y, self.x)]:
            J.disable = True
            self.top_show()
        
         
    def update(self):
        self.move()   
        self.root.after(500, self.update)
        
    def top_show(self):
        top = Toplevel()
        lbt = Label(top, text=self.color + " = " + str(self.count))
        lbt.pack()
        top.mainloop()
    
        
class M(P):
    def __init__(self, root, color, node, target, maps, ban):
        super().__init__(root, color, node, target, maps, ban)
        self.visit[node] += 1
        
    def move(self):
        yx = self.choice((self.y, self.x))
        
        self.show(self.y, self.x, 'white')    
        self.y = yx[0]
        self.x = yx[1]
        self.show(yx[0], yx[1], self.color)
        
        self.count +=1
        
        if P.target == P.hierarchy[(self.y, self.x)]:
            J.disable = True
            self.top_show()
        
    def choice(self, yx):
        v = []
        for i in P.neighbor[yx]:
            v.append((i, self.visit[i])) 
            
        v.sort(key = lambda x: x[1], reverse = False)
        v = [i for i in v if v[0][1] == i[1]]
        v = random.choice(v)
        self.visit[v[0]] += 1
        return v[0]
             
            
class N(M):
    def __init__(self, root, color, node, target, maps, ban):
        super().__init__(root, color, node, target, maps, ban)
        self.coincidence = 0
        
    def choice(self, yx):
        v = []
        for i in P.neighbor[yx]:
            v.append((i, self.visit[i]))
             
        d = []
        for l in v:
            c = P.hierarchy[l[0]]
            
            r = 0
            for i in range(len(P.target)):
                if c[i] == P.target[i]:
                    r +=1
                else: break 
                
            if r > self.coincidence:
                self.coincidence = r
                d = [l]
            if r == self.coincidence:
                d.append(l)
        
        if d: v = d 
           
        v.sort(key = lambda x: x[1], reverse = False)
        v = [i for i in v if v[0][1] == i[1]]
        v = random.choice(v)
        self.visit[v[0]] += 1
        return v[0]   
        
        
class K(P):
    def __init__(self, root, color, node, target, maps, ban, short=False):
        super().__init__(root, color, node, target, maps, ban)
        self.shortest = [None]*len(P.neighbor)**2
        
        for t in P.hierarchy:
            if P.hierarchy[t] == P.target:
                end = t
        
        if not short:
            self.allnode = self.find_path(node, end)
        else:
            if node == end:
                self.shortest = [node]
            else:
                self.find_short_path(node, end)
                self.allnode = self.shortest
        
    def find_path(self, node, end, path=[]):
        path = path + [node]
        if node == end:
            return path
            
        for v in P.neighbor[node]:
            if v not in path:
                newpath = self.find_path(v, end, path)
                if newpath: 
                    return newpath
                    
        
    def find_short_path(self, node, end, path=[]):
        path = path + [node]
        if node == end:
            return path
        
        for v in P.neighbor[node]:
            if v not in path:
                newpath = self.find_short_path(v, end, path)
                if newpath: 
                    #print("newpath =", newpath)
                    if len(newpath) <= len(self.shortest):
                        self.shortest = newpath
        
        
    def move(self):
        if self.count < len(self.allnode):
            y = self.allnode[self.count][0]
            x = self.allnode[self.count][1]

            self.show(self.y, self.x, 'white')    
            self.y = y
            self.x = x
            self.show(y, x, self.color)
                
            self.count +=1
                
            if P.target == P.hierarchy[(self.y, self.x)]:
                J.disable = True
                self.top_show()         
               

class J(P):
    def __init__(self, root, color, node, target, maps, ban):
        super().__init__(root, color, node, target, maps, ban)
        J.disable = False
        
    def move(self):
        if not J.disable:
            v = []
            for i in P.neighbor[(self.y, self.x)]:
                v.append(i)    
            y,x = random.choice(v)
            
            P.hierarchy[(self.y, self.x)] = '129'
            self.show(self.y, self.x, 'white')   
            self.y = y
            self.x = x
            P.hierarchy[(self.y, self.x)] = P.target
            self.show(y, x, self.color)
            
           

#--------- main ---------#    
if __name__ == "__main__":
    
    root = Tk()

    def update():
        p1.update()
        m1.update()
        n1.update()
        k1.update()
        k2.update()
        j1.update()

    target = ('122')
    ban=[(1,1), (1,2), (2,3)]

    maps = [ ["011", "012", "013", "211", "212", "201"],
             ["014", "015", "021", "213", "214", "202"],
             ["022", "023", "024", "215", "216", "203"],
             ["025", "026", "027", "213", "204", "205"],
             ["101", "102", "103", "121", "122", "123"],
             ["104", "105", "106", "124", "125", "126"]
    ]
    
    sizeY = len(maps)
    sizeX = len(maps[0])
       
    for y in range(sizeY):
        for x in range(sizeX):
            if (y, x) in ban:
                lb = Label(text=" ", background = 'black')
                lb.configure(text=maps[y][x])
            else:
                lb = Label(text=" ", background = 'white')
                lb.configure(text=maps[y][x])
            lb.grid(row=y, column=x, ipadx=10, ipady=5, padx=1, pady=1)

    p1 = P(root, 'red',  (1,0), target, maps, ban)
    m1 = M(root, 'blue',  (1,0), target, maps, ban)
    n1 = N(root, 'green',  (1,0), target, maps, ban)
    k1 = K(root, 'brown',  (1,0), target, maps, ban, short=True)
    k2 = K(root, 'violet',  (1,0), target, maps, ban)
    j1 = J(root, 'yellow',  (4,4), target, maps, ban)
            
    root.after(500, update)  
    root.mainloop()

