# -*- coding: utf-8 -*-

import numpy as np

class trait():
    def __init__(self,  x,y):
        self.x = x
        self.y = y
        self.plat = True
        self.last = True
        self.pj = 'P'
    def __sub__(s1,s2):
        x1,y1 = s1.getPoints()
        x2,y2 = s2.getPoints()
        
        if x1[0]>x2[0]:    
            h = y2[1]-y1[0]
        else:
            h = y1[1]-y2[0]
        return h
    def val(self):
        return np.average(self.y)
    def getmq(self):
        return np.polyfit(self.x, self.y, 1)
    def slope(self):
        m,q = self.getmq()
        return np.arctan(m)*180.0/np.pi
            
    def alen(self):
        return np.sqrt((self.x[-1]-self.x[0])**2+(self.y[-1]-self.y[0])**2)
    def hlen(self):
        return np.abs(self.x[-1]-self.x[0])
    
    def getPoints(self,mode='lin',polyorder=2):
        x = [self.x[0],self.x[-1]]
        if mode=='flat':
            y = [self.val(),self.val()]
        elif mode=='lin':
            m,q = self.getmq()
            y = [m*self.x[0]+q,m*self.x[-1]+q]
        elif mode=='poly':
            p = np.polyfit(self.x, self.y, polyorder)
            x = np.linspace(self.x[0],self.x[-1],num=50)
            y = np.polyval(p,x)
        return x,y

    
        
import savitzky_golay as sg
class segmentation():
    def __init__(self):
        self.slope=45
        self.filtorder=3
        self.mainth=1.5
        self.minlen=10
        self.zmin=0.0
        self.deltaF=5.0
        self.window= 2.0
        self.absth = None
        self.abswin = None
        self.delta = 3.0/5.0
        self.trorder = 1.0

    def run(self,p):
        #ifrom = np.argmax(p.f)
        x = p.z#[ifrom:]
        y = p.f#[ifrom:]

        
        self.abswin = int( self.window * float(len(x))/1000.0)
        
        y2 = sg.getSG(y,filtwidth=self.abswin,filtorder=self.filtorder,deriv=1)
        y3 = sg.getSG(y,filtwidth=self.abswin*self.delta,filtorder=self.filtorder,deriv=1)
        
        self.absth = np.std(y2-y3) * self.mainth
        
        return self.act(x,y)

    def act(self,x,y):
        """    
        mainth: threshold of the first derivative to identify steps    
        vth length above witch a segment is considered a plateau
        filtwidth,filtorder: width and order of the SG filter
        plath: distance from the origin of the first plateaux
        """
        #identification of the steps by first derivative peaks

        der = sg.getSG(y, self.abswin, self.filtorder, deriv=1)    
        xi = np.where(der<self.absth)
        
        segments = []                 
        bmleft = xi[0]-np.roll(xi[0],1)-1
        bmright = np.roll(xi[0],-1)-xi[0]-1
        bordermatrix = bmleft+bmright
        
        borders = np.where(bordermatrix!=0)[0]
    
        bmin = borders-np.roll(borders,1)
        bmax = borders-np.roll(borders,-1)
        btrue = borders[np.where(bmin+bmax != 0)]
    
    
        iborders = xi[0][btrue]
        np.append(0,iborders,len(der)-1)
          
        ibinv = iborders[::-1]
        previous = None
        for i in range(0,len(ibinv)-1,2):
            xx = x[ibinv[i+1]:ibinv[i]]
            yy = y[ibinv[i+1]:ibinv[i]]
            segfound=trait(xx,yy)
            
            if self.zmin>0 and xx[0]-x[0]<self.zmin:
                segfound.plat=False
            elif self.zmin<0 and x[0]-xx[0]<self.zmin:
                segfound.plat=False
            else:
                if segfound.hlen()<=self.minlen:
                    segfound.plat=False
                else:
                    if previous != None:
                        h = segfound-previous
                        if np.abs(h) < self.deltaF:
                            segfound.last = False
                        else:
                            previous = segfound
                    else:
                        previous = segfound
            segments.append(segfound)
    
        return segments