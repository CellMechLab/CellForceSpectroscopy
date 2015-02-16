"""
Created on Wed Aug  6 22:05:30 2014

@author: vassalli
"""
import numpy as np
import matplotlib.pyplot as plt

def gauss(x, *p):
    B, A, x0, C = p
    return B+A*np.exp(-((x-x0)/C)**2)

def decay(x, *p):
    A, B, x0 = p
    return A-B*np.exp(-x/x0) 

def bauss(x, *p):
    B, A1, A2, x1, x2, C1, C2 = p
    return B+A1**2*np.exp(-((x-x1)/C1)**2)+A2**2*np.exp(-((x-x2)/C2)**2)

def decfit(x,y,full=False):
    from scipy.optimize import curve_fit
    # p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
    
    p0 = [0.0,max(y), x[-1]/5.0]

    coeff, var_matrix = curve_fit(decay, x, y, p0=p0)        
    
    if full:
        xf = np.linspace(min(x),max(x),300)
        yf = decay(xf,*coeff)
        return coeff,xf,yf
    else:
        return coeff
 
def gaussfit(x,y,full=False,cfit=False):
    from scipy.optimize import curve_fit

    imax = np.argmax(y)
    
    xdove = np.where(y>(y[imax]-min(y))/1.3)[0]
    
    xx = x[xdove[0]:xdove[-1]]
    yy = y[xdove[0]:xdove[-1]]
    
    C = x[xdove[-1]]-x[xdove[0]]
    if C <= 0.0:
        C = 10.0
    p0 = [min(y),y[imax]-min(y), x[imax], C]

    if cfit:
        coeff, var_matrix = curve_fit(gauss, xx, yy, p0=p0)
    else:
        coeff, var_matrix = curve_fit(gauss, x, y, p0=p0)        
    
    if full:
        xf = np.linspace(min(x),max(x),300)
        yf = gauss(xf,*coeff)
        return coeff,xf,yf
    else:
        return coeff

def baussfit(x,y,full=False):
    from scipy.optimize import curve_fit

    imax = np.argmax(y)
    
    xdove = np.where(y>(y[imax]-min(y))/1.3)[0]
    
    xx = x[xdove[0]:xdove[-1]]
    yy = y[xdove[0]:xdove[-1]]
    
    C = x[xdove[-1]]-x[xdove[0]]
    dx = (x[-1]-x[0])/4.0
    if C <= 0.0:
        C = 10.0
    C1 = C2 = C
    a = np.sqrt(max(y)-min(y))
    p0 = [min(y),a,a, x[0]+dx,(x[-1]+x[0])/2.0, C1, C2]
    print p0
    coeff, var_matrix = curve_fit(bauss, x, y, p0=p0)        
    if full:
        xf = np.linspace(min(x),max(x),300)
        yf = bauss(xf,*coeff)
        return coeff,xf,yf
    else:
        return coeff


def readStats(fname):
    # c,L,P,H
    return np.loadtxt(fname,delimiter=';',usecols=(1,2,3,4),unpack=True)

def getVal(exp,col='H'):
    if col in ['c','L','P','H']:
        order = {'c':0,'L':1,'P':2,'H':3}
        col = order[col]
    v = []
    for ds in exp:
        v.append(ds[col])
    return v

def oneH(exp,w=0,val='H',bins=30,rng=(0,300),col='r',lab='1',fit=1, normed = True):
    v = getVal(exp,val)
    if rng == None:
        rng = (min(v[w]),max(v[w]))
    h,e = np.histogram(v[w],bins=bins,range=rng,density=normed)
    x = (e[1:]+e[:-1])/2.0
    if fit == 1:
		coeff,xf,yf = gaussfit(x,h,full=True)
    else:
		coeff,xf,yf = baussfit(x,h,full=True)
    co = col+'o'
    plt.plot(x,h,co,label=lab)
    co = col + '--'
    plt.plot(xf,yf,co)
    plt.xlabel('Step height [nm]')
    plt.ylabel('Density of occurrence')
    return coeff
speeds = np.array([1,2.5,10,25,50])
labels = ['1','2.5','10','25','50']   

def oneL(exp,w=0,val='L',bins=50,rng=(0,10000),col='r',lab='1',sim='o'):
    v = getVal(exp,val)
    if rng == None:
        rng = (min(v[w]),max(v[w]))
    h,e = np.histogram(v[w],bins=bins,range=rng,density=True)
    x = (e[1:]+e[:-1])/2.0
    coeff,xf,yf = decfit(x,h,full=True)
    co = col+sim
    plt.plot(x,h,co,label=lab)
    co = col + '--'
    plt.plot(xf,yf,co)
    plt.xlabel('Step Length [nm]')
    plt.ylabel('Density of occurrence')
    return coeff
    
def oneT(exp,speed= 1.0, w=0,bins=50,rng=None,col='r',lab='1',sim='o',normed=True,fromStart=False):
    vL = np.array(getVal(exp,'L'))
    vP = np.array(getVal(exp,'P'))
    if rng == None:
        if fromStart:
            h,e = np.histogram((vL[w]+vP[w])/speed,bins=bins,density=normed)
        else:
            h,e = np.histogram((vL[w])/speed,bins=bins,density=normed)
    else:
        if fromStart:
            h,e = np.histogram((vL[w]+vP[w])/speed,bins=bins,range=rng,density=normed)
        else:
            h,e = np.histogram((vL[w])/speed,bins=bins,range=rng,density=normed)
    x = (e[1:]+e[:-1])/2.0
    coeff=1.0
    #coeff,xf,yf = decfit(x,h,full=True)
    co = col+sim
    plt.plot(x,h,co,label=lab)
    co = col + '--'
    #plt.plot(xf,yf,co)
    plt.xlabel('Lifetime [s]')
    plt.ylabel('Density of occurrence')
    return coeff

def oneE(exp,speed= 1.0, w=0,val='L',bins=50,rng=None,col='r',lab='1',sim='o',normed=True):
    v1 = np.array(getVal(exp,'L'))
    v2 = np.array(getVal(exp,'H'))
    
    E = np.array(v1[w])*np.array(v2[w])
    
    if rng == None:
        rng = (min(E),max(E))
    h,e = np.histogram(E,bins=bins,range=rng,density=normed)
    x = (e[1:]+e[:-1])/2.0
    coeff=1.0
    #coeff,xf,yf = decfit(x,h,full=True)
    co = col+sim
    plt.plot(x,h,co,label=lab)
    co = col + '--'
    #plt.plot(xf,yf,co)
    plt.xlabel('Energy [pN nm]')
    plt.ylabel('Density of occurrence')
    return coeff
    
speeds = np.array([1,2.5,10,25,50])
labels = ['1','2.5','10','25','50']   
 
def allH(exp,bins=50,rng=(0,200),k=1.0,col='r', fit = 1, normed = True):
    plt.figure()
    cols = ['r','b','g','y','c']
    if fit==1:
		x0 = []
    else:
		x1=[]
		x2=[]
    for i in range(5):    
        coe = oneH(exp,w=i,val='H',bins=bins,rng=rng,col=cols[i],lab=labels[i],fit=fit, normed = normed)
        if fit==1:
			x0.append(coe[2])
        else:
			x1.append(coe[3])
			x2.append(coe[4])
    plt.legend()
    plt.figure(10)
    plt.xlabel('Speed [um/s] - LOG scale')
    plt.ylabel('Height [nm]')    
    if fit==1:
		plt.plot(np.log(speeds),x0,col+'o')
		return np.array(x0)/k
    else:
		plt.plot(np.log(speeds),x1,col+'o')
		plt.plot(np.log(speeds),x2,col+'*')
		return np.array(x1)/k,np.array(x2)/k

def allL(exp,bins=10,rng=(0,5000),sim='o'):
    plt.figure(1)    
    cols = ['r','b','g','y','c']
    x0 = []
    for i in range(5):    
        coe = oneL(exp,w=i,bins=bins,rng=rng,col=cols[i],lab=labels[i],sim=sim)
        x0.append(coe[2])
    plt.legend()
    plt.figure(2)
    plt.xlabel('Speed [um/s]')
    plt.ylabel('Decay Length [nm]')    
    plt.plot(speeds,x0,'r'+sim)
    return x0
    
def allT(exp,bins=10,rng=None,sim='o',normed=False,fs=False):
    plt.figure(1)    
    cols = ['r','b','g','y','c']
    x0 = []
    vels=[1.0,2.5,10.0,25.0,50.0]
    for i in range(5):    
        v=vels[i]*1000.0
        oneT(exp,speed=v,w=i,bins=bins,rng=rng,col=cols[i],lab=labels[i],sim=sim,normed=normed,fromStart=fs)
        #x0.append(coe[2])
        x0.append(1.0)
    plt.legend()
    plt.figure(2)
    plt.xlabel('Speed [um/s]')
    plt.ylabel('Decay Length [nm]')    
    plt.plot(speeds,x0,'r'+sim)
    return x0
    
def allE(exp,bins=10,rng=None,sim='o',normed=True):
    plt.figure(1)    
    cols = ['r','b','g','y','c']
    x0 = []
    vels=[1.0,2.5,10.0,25.0,50.0]
    for i in range(5):    
        v=vels[i]*1000.0
        coe = oneE(exp,speed=v,w=i,bins=bins,rng=rng,col=cols[i],lab=labels[i],sim=sim,normed=normed)
        #x0.append(coe[2])
        x0.append(1.0)
    plt.legend()
    plt.figure(2)
    plt.xlabel('Speed [um/s]')
    plt.ylabel('Decay Length [nm]')    
    plt.plot(speeds,x0,'r'+sim)
    return x0
    
def readres(name = 'e1'):
    exp = []
    for l in labels:
        nm = 'res/{0}'.format(name)+l+'.txt'
        c,L,P,H = readStats(nm)
        exp.append([c,L,P,H])
    return exp
    

def prova(exp,tL = 7000,tP = 27000,col='r'):
    for i in range(5):
        lab = labels[i]
        H=[]
        e = exp[i]
        for j in range(len(e[1])):
            if e[1][j]>=tL and e[2][j]>=tP:
                H.append(e[3][j])
        xH = speeds[i]*np.ones(len(H))
        plt.plot(xH,H,col+'o',label=lab)
    plt.legend()

def prova2(exp,tL = 7000,tP = 27000,col='r'):
    Hall=[]
    for i in range(5):
        H=[]
        e = exp[i]
        for j in range(len(e[1])):
            d1 = False
            d2 = False
            if (e[1][j]>=tL and tL>=0) or (e[1][j]<=-tL and tL<0):
                d1=True
            if (e[2][j]>=tP and tP>=0) or (e[2][j]<=-tP and tP<0):
                d2=True
            if d1 and d2:
                H.append(e[3][j])
        Hall.append(H)
    
    plt.boxplot(Hall,positions=np.log(speeds))

def numpeaks(exp):
    Hall=[]
    for i in range(5):
        H=[]
        e = exp[i]
        pc = 0
        ac = 0
        for j in e[0]:
            if j == pc:
                ac += 1
            else:
                if ac!=0:
                    H.append(ac)
                ac = 1
                pc = j
        if ac!=0:
            H.append(ac)
        Hall.append(H)
    
    plt.boxplot(Hall,positions=np.log(speeds))

    
def riprovo(e,col='r',lab='e1'):
    for i in range(5):
        plt.plot(e[i][1],e[i][2],col+'o',alpha=0.1,label=lab,markersize=6)

def riprovo2(e,col='r',lab='e1',w=1):
    for i in range(5):
        plt.plot(e[i][w],e[i][3],col+'o',alpha=0.33,label=lab,markersize=5)
              
def riprovo3(e,col='r',lab='e1'):
    x = []
    xx = 0
    y = []
    for i in range(5):
        for j in range(len(e[i][0])):
            y.append(e[i][3][j])
            x.append(xx+e[i][0][j])
        xx = x[-1]
        plt.plot(x,y,'o',alpha=0.33,label=lab,markersize=5)
        x=[]
        y=[]
        
    
pre = ['e1e','e2e','ene']
