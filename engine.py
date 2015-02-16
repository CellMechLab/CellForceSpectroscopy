import numpy as np
import savitzky_golay as sg 

def getSG(y,filtwidth=21,filtorder=2,deriv=1):
    if filtwidth < filtorder + 2:
        filtwidth = filtorder + 3
        if filtwidth % 2 == 0:
            filtwidth +=1
        print 'WARN: window size reset to {0}'.format(filtwidth)
    return sg.savitzky_golay(y, filtwidth, filtorder, deriv=deriv)

def getWeight(y):
    
    yc = y[int(len(y)/3):-int(len(y)/6)]
    return np.std(yc)
    yc=y
    import pylab
    c = pylab.hist(y,bins=100)
    yy = c[0]
    xx = (c[1][1:]+c[1][:-1])/2
    
    def gaus(x,a,x0,sigma):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))
    n = len(xx)                          #the number of data
    mean = sum(xx*yy)/n                   #note this correction
    sigma = sum(yy*(xx-mean)**2)/n        #note this correction
    from scipy.optimize import curve_fit
    popt,pcov = curve_fit(gaus,xx,yy,p0=[1,mean,sigma])
    
    pylab.plot(xx,gaus(xx,*popt),'r--')
    pylab.show()
    
    return np.var(yc)

class seg():
    def __init__(self,  x,y):
        self.x = x
        self.y = y
        self.plat = True
        self.last = True
    def val(self):
        return np.average(self.y)
    def getmq(self):
        return np.polyfit(self.x, self.y, 1)
        
    def len(self):
        return np.sqrt((self.x[-1]-self.x[0])**2+(self.y[-1]-self.y[0])**2)
    def hlen(self):
        return np.abs(self.x[-1]-self.x[0])
    
    def getPoints(self,flat=False):
        x = [self.x[0],self.x[-1]]
        if flat:
            y = [self.val(),self.val()]
        else:
            m,q = self.getmq()
            y = [m*self.x[0]+q,m*self.x[-1]+q]
        return x,y
    


def act(x,y,mainth = 1.0,vth = 0.0,filtwidth = 21,filtorder = 2,plath=1000.0,lasth = 10.0):
    """    
    mainth: threshold of the first derivative to identify steps    
    vth length above witch a segment is considered a plateau
    filtwidth,filtorder: width and order of the SG filter
    plath: distance from the origin of the first plateaux
    """
    #identification of the steps by first derivative peaks
    der = getSG(y, filtwidth, filtorder, deriv=1)

    xi = np.where(der<mainth)
    
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
        segfound=seg(xx,yy)
        
        if plath>0 and xx[0]-x[0]<plath:
            segfound.plat=False
        elif plath<0 and x[0]-xx[0]<plath:
            segfound.plat=False
        else:
            if segfound.hlen()<=vth:
                segfound.plat=False
            else:
                if previous != None:
                    h = getH (segfound,previous)
                    if np.abs(h) < lasth:
                        segfound.last = False
                    else:
                        previous = segfound
                else:
                    previous = segfound
        segments.append(segfound)

    return segments

def getH(s1,s2):
    x1,y1 = s1.getPoints()
    x2,y2 = s2.getPoints()
    
    if x1[0]>x2[0]:    
        h = y2[1]-y1[0]
    else:
        h = y1[1]-y2[0]
    return h

def getStat(segs):
    L=[]
    P=[]
    H=[]
    n=0
    pL = 0
    pMin = 0
    prev = None
    for s in segs:
        if s.plat:
            if s.last:
                n=n+1
                if n>1:
                    L.append(pL)
                    P.append(pMin)
                    H.append(getH(s,prev))
                    pL = s.len()
            else:
                pL += s.len()
            pMin = min(s.x)
            prev=s
    return n,L,P,H        

def readStats(fname):
    # c,L,P,H
    return np.loadtxt(fname,delimiter=';',usecols=(1,2,3,4),unpack=True)
    
    
def execution():

    pz = []
    ln = []
    dz=[]
    cvi = 0
    mainth = 1.0
    thresh = 100.0
    vth = 0.0
    filtwidth = 51
    filtorder = 2
    for c in cv:
        if len(c)>0:
            cvi +=1
            x = c[2].z
            y = c[2].f
    
            ifrom = np.argmax(y)
            
            x = x[ifrom:]
            y = y[ifrom:]
            
            pylab.subplot(2,2,cvi)
            pylab.plot(x,y,'k.')
            pylab.title(c.basename)
            der = sg.savitzky_golay(y, filtwidth, filtorder, deriv=1)
            xi = np.where(der>mainth)
            
            segments = []
                    
                    
            js=[]    
            trovati = xi[0]  
            for j in range(len(y)):
                if j in trovati:
                    if len(js)>0:
                        xx = x[js]
                        yy = y[js]
                        segments.append(seg(xx,yy))
                    js = []        
                else:
                    js.append(j)
            if len(js)>0:
                    xx = x[js]
                    yy = y[js]
                    segments.append(seg(xx,yy))
            
            i=1
            
            for s in segments:
                if s.len()>vth:
                    s.plot(i,False)
                    i=i+1
                if s.len()>thresh:
                    pz.append(s.val())
                    ln.append(s.len())
            
            prev=segments[-1].val()
            for s in segments[::-1]:
                if s.len()>thresh:
                    if s.val() != prev:
                        dz.append(s.val()-prev)    
                        prev = s.val()
