import numpy as np
from . import mvobject
from scipy.integrate import trapz

from scipy.signal import savgol_filter as sg
def getSG(y,filtwidth=21,filtorder=2,deriv=1):
    filtwidth = int(filtwidth)
    if filtwidth < filtorder + 2:
        filtwidth = filtorder + 3
    if filtwidth % 2 == 0:
        filtwidth +=1
        #print 'WARN: window size reset to {0}'.format(filtwidth)
    try:
        o = sg(y, filtwidth, filtorder, deriv=deriv)
    except:
        print ('Error filtering',len(y),filtwidth,filtorder)
        return y
    return o

class segment(mvobject.mvobject):
    def __init__(self, x=None, y=None):
        #internal units
        #  sensitivity nm/V
        #  k pN/nm
        #  speed nm/s
        #  Z nm
        #  F pN
        #  directions are near | far | hold
        defaults = {
            'direction': 'far',
            'speed': 0.0,
            'k': 1.0,
            'type': 'Vconst',
            'duration': 0.0,
            'setpoint': 0.0,
            'zstart':0.0,
            'zend':0.0
        }
        self.direction= 'far'
        self.speed= 0.0
        self.k= 1.0
        self.type= 'Vconst'
        self.duration= 0.0
        self.setpoint= 0.0
        self.zstart=0.0
        self.zend=0.0
        self.parseConfig(defaults, 'Segment')
        self.show = True
        self.traits = []
        self._x=[]
        self._y=[]
        self.z = np.array([])
        self.f = np.array([])
        if x is not None and y is not None:
            self.setXY(x,y)

    def setSpeed(self,speed=None):
        if speed is None:
            delta = np.abs(self.zstart-self.zend)
            if self.duration != 0:
                self.speed = delta/self.duration
            else:
                self.speed = 0.0
        else:
            self.speed=speed
        
    def setXY(self,x=None,y=None):
        if x is None:
            x,y = self._x,self._y
        if len(x)==0 or len(y)==0:
            return
        if x[0] > x[-1]:
            self.direction = 'near'
            x.reverse()
            y.reverse()        
        self.z = np.array(x)
        self.f = np.array(y)
        self._x,self._y=None,None

    def getRelevant(self,val=0.0):
        for i in range(len(self.z)):
            if self.z[i] >= val:
                start = i
                break
        return self.z[start:], self.f[start:]

    def FZtoFD(self):
        """
        Convert Force versus Displacement to Force versus Distance
        """
        self.z = self.z - self.f / self.k

    def getContactIndex(self, smooth=True,val = 0.0):
        y = self.f
        if smooth is True:
            y = getSG(self.f, len(self.f / 100), 2, 0)
        if y[0]>=val:
            return 0
        for i in range(len(y) - 1):
            if ((y[i] + 1 > val) and (y[i] < val)):
                return i + 1
        return 0    

    def getNumbers(self):
        nump = 0
        numj = 0
        numb = 0
        for i in range(len(self.traits)):
            t = self.traits[i]
            if t.accept:
                if t.pj == 'P':
                    nump += 1
                else:
                    numj += 1
            else:
                numb += 1
        return nump, numj, numb

    def getStretchTo(self,toDistance):
        from scipy import interpolate
        x = self.z
        y = self.f
        x0,y0 = self.getOrigin()
        rep = interpolate.splrep(x, y)
        return interpolate.splint(x0, x0+toDistance, rep)

    def getStretchArea(self,toJump=False):
        x = self.z
        y = self.f

        istart = self.getOrigin(True)

        if toJump is True:
            iend = self.getNearFarPoint(True)
        else:
            iend = self.getJumpPoint(True)

        if istart >= iend:
            return 0
        
        from scipy.integrate import trapz
        area = trapz(y[istart:iend], x[istart:iend])
        return area

    def getArea(self, reflatten=False, polyorder=2):
        """
        :rtype : float
        """
        x = self.z
        y = self.f

        istart = self.getOrigin(True)

        if reflatten and len(self.traits) > 0:
            p = np.polyfit(self.traits[0].x, self.traits[0].y, polyorder)
            y = y - np.polyval(p, x)

        from scipy.integrate import trapz
        return trapz(y[istart:], x[istart:])

    def getMaxStep(self,filter=False,rngX=[-9999,99999],rngLen=[0,99999]):
        if len(self.traits)==0:
            return 0.0

        data = []
        j=0
        pret = self.traits[0]
        for t in self.traits:
            if t.accept is True and j>0:
                number = t-pret
                pret = t
                if filter is True:
                    if (rngX[0] < min(t.x) < rngX[1]):
                        if (rngLen[0] < t.alen() < rngLen[1]):
                            data.append(number)
                else:
                    data.append(number)
            j+=1
        if len(data)==0:
            return 0.0
        return max(data)

    def zShift(self,val):
        self.traits = []
        self.z -= val

    def fShift(self,val):
        self.traits = []
        self.f -= val

    def rescale(self,m):
        self.traits = []
        self.f /= m

    def getOrigin(self,indexonly=False):
        u = self.getUltimi()
        if len(u)==0:
            if np.min(self.f)<0.0<np.max(self.f):
                fshift = 0.0
            else:
                fshift = np.average(self.f)
        else:
            fshift = np.average(self.f[ u[-1].imin:u[0].imax ] )

        dove = 0
        beg = self.f[0]<fshift
        for i in range(len(self.z)):
            now = self.f[i]<fshift
            if now is not beg:
                dove = i
                break
        if indexonly is True:
            return dove
        zshift = self.z[dove]
        #print(dove,zshift,fshift)
        return zshift,fshift

    def hasFished(self,forceThreshold,toJump=False,detachOnly=False):
        if detachOnly is True:
            if self.getDetachForce()>forceThreshold:
                return True
            return False 
        else:
            y0 = self.getOrigin()[1]
            if toJump is True:
                y1 = self.getNearFarPoint()[1]
            else:
                y1 = self.getJumpPoint()[1]
            if (np.abs(y1-y0)>forceThreshold):
                return True
            return False

    def getUltimi(self):
        if len(self.traits) <2:
            return []
        ultimi = []
        for t in self.traits:
            if t.accept is True:
                ultimi.append(t)
                if t.last is True:
                    return ultimi
        return []

    def getUltimiPenultimi(self):
        if len(self.traits) <2:
            return [],[]
        ultimi = []
        penultimi = []
        ultimo = True
        for t in self.traits:
            if ultimo is True:
                if t.accept is True:
                    ultimi.append(t)
                    if t.last is True:
                        ultimo = False
            else:
                if t.accept is True:
                    penultimi.append(t)
                    if t.last is True:
                        return ultimi,penultimi
        return [],[]

    def getJumpSlope(self):
        p = self.getUltimiPenultimi()[1]
        if len(p)==0:
            return 0
        return p[-1].slope(angle=False)
        
    def getNearFarPoint(self,indexonly=False):
        if len(self.traits) <2:
            i = np.argmax(self.f)
            if indexonly is True:
                return i
            return [self.z[i],self.f[i]]
        for t in self.traits:
            if t.accept is True and t.pj=='J':
                i = np.argmax(t.x)
                if indexonly is True:
                    return t.imin+i
                return t.x[i],t.y[i]
        i = np.argmax(self.f)
        if indexonly is True:
            return i
        return [self.z[i],self.f[i]]

    def getJumpPoint(self,indexonly=False):
        u,p = self.getUltimiPenultimi()
        if len(u)==0 or len(p)==0:
            if indexonly is True:
                return np.argmax(self.f)
            return self.z[np.argmax(self.f)],np.max(self.f)
        x = self.z[p[0].imax:u[-1].imin]
        y = self.f[p[0].imax:u[-1].imin]
        if indexonly is True:
            return p[0].imax+np.argmax(y)
        return x[np.argmax(y)],np.max(y)

    def getDetachPoint(self):
        return self.getJumpPoint()[0]

    def getDetachForce(self):
        return self.getJumpPoint()[1]

    def getAdhesion(self):
        return np.max(self.f)


if __name__ == "__main__":
    print('not for direct use')
