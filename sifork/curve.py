from . import mvobject
from . import segment
import numpy as np
import logging
import importlib
import os
import glob

class curve(mvobject.mvobject):
    def __init__(self,  fname = None, family = 1):
        #internal units
        #  sensitivity nm/V
        #  k pN/nm
        #  speed nm/s
        #  Z nm
        #  F pN
        defaults = {'fzfd':False,'k':1.0, 'relevant':True, 'sensitivity': 50.0}
        self.fzfd = False
        self.k = 1.0
        self.relevant = True
        self.sensitivity = 50.0
        self.parseConfig(defaults,'Curve')

        self.filename = ''
        self.basename = ''
        self.segments=[]
        self.info={}
        self.family = family
        self.flattened = False
        self.recalibrated = False

        self.custom = False
        self.customSegmentation = None

        if fname is not None:
            self.filename = fname
            self.basename = os.path.basename(fname)
            self.open(fname)
        return
    def __iter__(self):
        return self.segments.__iter__()
    def __nonzero__(self):
        return self.relevant
    def __len__(self):
        return len(self.segments)
    def __getitem__(self, index):
        if index=='down':
            iz = self.getAZ('down')
            if iz is None:
                raise (IndexError)
            return self.segments[iz]
        if index == 'up':
            iz = self.getAZ('up')
            if iz is None:
                raise (IndexError)
            return self.segments[iz]
        if len(self.segments) == 0:
            raise (IndexError)
        return self.segments[index]

    def append(self,seg):
        if isinstance(seg,segment.segment):
            self.segments.append(seg)
        else:
            logging.error('You need to append a full instance of segment')
            
    def getAZ(self,w):
        if w=='up':
            iz=None
            for j in range(len(self.segments)):
                if self.segments[j].direction=='far':
                    iz=j
            return iz
        elif w=='down':
            for j in range(len(self.segments)):
                if self.segments[j].direction=='near':
                    return j
            return None
        return None

    def getJumpPoint(self,idonly=False):
        return self['up'].getJumpPoint(idonly)

    def getDetachPoint(self):
        return self['up'].getDetachPoint()

    def getJumpSlope(self):
        return self['up'].getJumpSlope()

    def getDetachForce(self):
        return self['up'].getDetachForce()
        
    def getNearFarPoint(self,idonly=False):
        return self['up'].getNearFarPoint(idonly)

    def getStretchArea(self,idonly=False):
        return self['up'].getStretchArea(idonly)

    def recalibrateContactRegion(self):
        zs = self['up'].getOrigin()[0]
        icontact = np.argmin((self['up'].z-zs)**2)
        x = self['up'].z[:icontact]
        y = self['up'].f[:icontact]/self.k
        m=np.polyfit(x, y, 1)[0]
        for seg in self:
            if seg.f is not None and len(seg.f)>0:
                seg.rescale(m)
        self.recalibrated = True

    def flatten(self):
        if self['up'].f is not None and len(self['up'].f)>0:
            zs,fs = self['up'].getOrigin()
            for seg in self:
                if seg.f is not None and len(seg.f)>0:
                    seg.zShift(zs)
                    seg.fShift(fs)
        self.flattened = True
        
    def hasFished(self,forceThreshold=None,toJump=False):
        return self['up'].hasFished(forceThreshold,toJump)

    def isEmpty(self):
        if len(self.segments)==0:
            return True
        i=self.getAZ('up')
        if i is None:
            return True
        if len(self.segments[i].f)==0:
            return True
        return False

    def open(self,fname,driver=None):
        if not os.path.isfile(fname):
            logging.error("The file {0} does not exist".format(fname))
            return False

        #search for the specific driver
        from . import open_all as opa
        op = opa.opener(fname)
        try:
            parameters,info,segments=op.getOpener(driver)
        except:
            raise

        if len(segments)==0:
            logging.error("Empty File {0} not appended".format(fname))
            return False

        for k,v in parameters.items():
            setattr(self,k,v)
        self.info = info
        for s in segments:
            self.append(s)

    def save(self,fname=None):
        """
        Save the curve in a TXT format compatible with the text export format of JPK IP and DP programs
        """
        if fname == None:
            return False

        out_file = open(str(fname),"w")
        out_file.write("# TEXT EXPORT\n")
        out_file.write("# springConstant: {0}\n".format(self.k))
        out_file.write("# units: m N\n")
        if self.fzfd:
            out_file.write("# fzfd: 1\n")
        else:
            out_file.write("# fzfd: 0\n")
        out_file.write("#\n")
        i=0
        for p in self:
            if i != 0:
                out_file.write("\n")
            out_file.write("#\n")
            out_file.write("# segmentIndex: {0}\n".format(i))
            ts = 'extend'
            if p.direction == 'B':
                ts = 'retract'
            out_file.write("# segment: {0}\n".format(ts))
            out_file.write("# columns: distance force\n")
            out_file.write("# speed: {0}\n".format(p.speed))
            for i in range(len(p.x)):
                out_file.write("{0} {1}\n".format(p.x[i]*1e-9, -1.0*p.y[i]*1e-12))
            i+=1
        out_file.close()
        return True

if __name__ == "__main__":
    print ( 'not for direct use' )
