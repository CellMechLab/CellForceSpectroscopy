"""
Created on Fri Nov 28 18:46:09 2014

@author: vassalli
"""

from SiMPlE import experiment
import engine
import os
import numpy as np

def gauss(x, *p):
    B, A, x0, C = p
    return B+A*np.exp(-((x-x0)/C)**2)
def gaussfit(x,y,full=False,cfit=False):
    from scipy.optimize import curve_fit
    # p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
    imax = np.argmax(y)
    
    xdove = np.where(y>(y[imax]-min(y))/1.3)[0]
    
    xx = x[xdove[0]:xdove[-1]]
    yy = y[xdove[0]:xdove[-1]]
    
    C = x[xdove[-1]]-x[xdove[0]]
    if C <= 0.0:
        C = 1.0
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

class myAct():
    def __init__(self):
        self.exp = experiment.experiment()
        self.N=[]
        self.L=[]
        self.P=[]
        self.H=[]
        self.curG = 0
        
        self.sg_fw = 1.0
        self.sg_fo = 3
        self.s_mth = 2.0
        self.s_vth = 200.0
        self.plath = 2000.0
        self.lasth = 2.0
        
        self.speed = 1.0

    def fitG(self,v=None,bins=30,rng=None,full=False):
        if v == None:
            v = self.H
        # rng = (0,300)
        if rng == None:
            rng = (min(v),max(v))
        h,e = np.histogram(v,bins=bins,range=rng,density=True)
        x = (e[1:]+e[:-1])/2.0
        coeff,xf,yf = gaussfit(x,h,full=True)
        #center is coe[2]
        if Full:
            return coeff
        return coeff[2]

               
    def clearAll(self):
        self.exp = experiment.experiment()
        self.N=[]
        self.L=[]
        self.P=[]
        self.H=[]
        self.curG = 0
    def saveStats(self,fname):
        
        out_file = open(str(fname),"w")
        out_file.write("# STATS EXPORT\n")

        out_file.write("# {0}:{1}\n".format('WindowSize',self.sg_fw))
        out_file.write("# {0}:{1}\n".format('SGOrder',self.sg_fo))
        out_file.write("# {0}:{1}\n".format('DerThreshold',self.s_mth))
        out_file.write("# {0}:{1}\n".format('MinLength',self.s_vth))
        out_file.write("# {0}:{1}\n".format('PlateauxLengthThreshold',self.plath))
        out_file.write("# {0}:{1}\n".format('He7ightJumpThreshold',self.lasth))
        out_file.write("# {0}:{1}\n".format('Speed',self.speed))
        out_file.write("# fname;curveN;L;P;H\n")
        
        j=0
        for c in self.exp:
            j+=1
            st = c.stats
            if st != None:
                for i in range(len(st['L'])):
                    out_file.write("{0};{1};{2};{3};{4}\n".format(c.filename,j,st['L'][i],st['P'][i],st['H'][i]))
        
        out_file.close()

    def doStats(self):
        self.N=[]
        self.L=[]
        self.P=[]
        self.H=[]
        
        for c in self.exp:
            p = c[-1]
            ifrom = np.argmax(p.f)
            x = p.z[ifrom:]
            y = p.f[ifrom:]
            sg_fw = int( self.sg_fw * len(x)/100.0)
            if sg_fw % 2 == 0:
                sg_fw+=1
            y2 = engine.getSG(y,filtwidth=sg_fw,filtorder=self.sg_fo,deriv=1)
            mth = np.std(y2) * self.s_mth

            segs = engine.act(x,y,mainth = mth,vth = self.s_vth,filtwidth = sg_fw,filtorder = self.sg_fo,plath=self.plath,lasth=self.lasth)
            
            n,L,P,H = engine.getStat(segs)
            
            if n>1:
                self.N.append(n)
                self.L.extend(L)
                self.P.extend(P)
                self.H.extend(H)
                c.stats = {}
                c.stats['L']=L
                c.stats['P']=P
                c.stats['H']=H
            else:
                c.stats = None
        
    def addFiles(self, fnames = None):
        for fname in fnames:
            self.exp.addFiles([str(fname)])
            
    def addDirectory(self,dirname=None):
        for fnamealone in os.listdir(dirname):
            fname = os.path.join(str(dirname), fnamealone)
            self.exp.addFiles([str(fname)])

def go(pars=None):
    dirs = ['exp1','exp2','ExpCHO-CHO_5min']
    vels = [1,2.5,10,25,50]
    nams = ['m1','m2','mn']
    
    for i in range(3):
        d = dirs[i]
        n = nams[i]
        for v in vels:
            e = myAct()
            if pars != None:
                for k, v in pars.iteritems():
                    setattr(e, k, v)
            e.addDirectory(d+'/'+str(v))
            e.doStats()
            e.saveStats('res/'+n+str(v)+'.txt')
            print 'dir: {0} v: {1}'.format(d,v)


if __name__ == "__main__":
    go()
