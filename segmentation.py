# -*- coding: utf-8 -*-

import numpy as np

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

class trait():
    def __init__(self, x, y,imin,imax):
        self.x = x
        self.y = y
        self.imin=imin
        self.imax=imax
        self.accept = True
        self.last = True
        self.first = True
        self.pj = 'P'
        self.height = None

    def __sub__(s1, s2):
        x1, y1 = s1.getPoints()
        x2, y2 = s2.getPoints()

        if x1[0] > x2[0]:
            h = y2[1] - y1[0]
        else:
            h = y1[1] - y2[0]
        return h

    def reject(self):
        self.accept = False
        self.first = False
        self.last = False

    def val(self):
        if len(self.y)<2:
            return 0.0
        return np.average(self.y)

    def getmq(self):
        if len(self.y)<2:
            return 0.0,0.0
        return np.polyfit(self.x, self.y, 1)

    def slope(self,angle=True):
        if len(self.y)<2:
            return 0.0
        m, q = self.getmq()
        if angle is True:
            return np.arctan(m) * 180.0 / np.pi
        else:
            return m

    def alen(self):
        if len(self.y)<2:
            return 0.0
        return np.sqrt((self.x[-1] - self.x[0])**2 + (self.y[-1] - self.y[0])**
                       2)
    def hlen(self):
        if len(self.y)<2:
            return 0.0
        return np.abs(self.x[-1] - self.x[0])

    def getPoints(self, mode='lin', polyorder=2, extend=False):
        x = [self.x[0], self.x[-1]]
        if mode == 'flat':
            y = [self.val(), self.val()]
        elif mode == 'lin':
            m, q = self.getmq()
            if extend is True:
                x = [0, self.x[-1]]
            y = [m * x[0] + q, m * x[-1] + q]
        elif mode == 'poly':
            p = np.polyfit(self.x, self.y, polyorder)
            if extend is True:
                x = np.linspace(0.0, self.x[-1], num=50)
            else:
                x = np.linspace(self.x[0], self.x[-1], num=50)
            y = np.polyval(p, x)
        elif mode=='curve':
            return self.x,self.y
        return x, y




class segmentation():
    def __init__(self):
        self.slope = 45
        self.filtorder = 3
        self.mainth = 1.5
        self.minlen = 10
        self.zmin = 0.0
        self.deltaF = 5.0
        self.window = 2.0
        self.delta = 3.0 / 5.0
        self.trorder = 1.0

    def abswin(self, p):
        awin = int(self.window * float(len(p.z)) / 1000.0)
        if awin < 5.0:
            return 5.0
        return awin

    def absth(self, p):
        window = self.abswin(p)
        y2 = getSG(p.f, filtwidth=window, filtorder=self.filtorder, deriv=1)
        y3 = getSG(
            p.f,
            filtwidth=window * self.delta,
            filtorder=self.filtorder,
            deriv=1)
        return np.std(y2 - y3) * self.mainth

    def run(self, p, debug=False):
        """
        mainth: threshold of the first derivative to identify steps
        vth length above witch a segment is considered a plateau
        filtwidth,filtorder: width and order of the SG filter
        plath: distance from the origin of the first plateaux
        """
        #identification of the steps by first derivative peaks
        #x,y=p.z,p.f
        derthresh = self.absth(p)
        der = getSG(p.f, self.abswin(p), self.filtorder, deriv=1)
        segments = []

        xi = np.arange(len(der))
        nw = np.logical_and(der >= -derthresh, der <= derthresh)
        q = np.zeros(len(xi))
        q[nw] = 1
        iborders = xi[np.logical_xor(q - np.roll(q, 1) == 1, q - np.roll(
            q, -1) == 1)]
        if -derthresh <= der[0] <= derthresh:
            if len(iborders) > 0:
                if iborders[0] != 0:
                    iborders = np.append(0, iborders)
            else:
                iborders = np.append(0, iborders)
        if -derthresh <= der[-1] <= derthresh:
            if len(iborders) > 0:
                if iborders[-1] != xi[-1]:
                    iborders = np.append(iborders, xi[-1])
        if debug is True:
            return iborders

        ibinv = iborders[::-1]
        previous = None
        #print('iborders {}'.format(iborders))
        for i in range(0, len(ibinv) - 1, 2):
            xx = p.z[ibinv[i + 1]:ibinv[i]]
            yy = p.f[ibinv[i + 1]:ibinv[i]]
            segfound = trait(xx, yy,ibinv[i + 1],ibinv[i])

            if self.zmin > 0 and xx[0] - p.z[0] < self.zmin:
                segfound.reject()
            elif self.zmin < 0 and p.z[0] - xx[0] < self.zmin:
                segfound.reject()
            else:
                if np.abs(segfound.slope()) < self.slope:
                    segfound.pj = 'P'
                else:
                    segfound.pj = 'J'
                if segfound.hlen() <= self.minlen:
                    segfound.reject()
                else:
                    if previous != None:
                        h = segfound - previous
                        segfound.height = h
                        if np.abs(h) < self.deltaF:
                            segfound.last = True
                            segfound.first = False
                            previous.last = False
                        #    previous = segfound
                        else:
                            segfound.first = True
                            segfound.last = True
                        previous = segfound
                    else:
                        segfound.first = True
                        segfound.last = True
                        previous = segfound

            segments.append(segfound)

        return segments
