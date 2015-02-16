from SiMPlE.qt import qtView
from SiMPlE import experiment
from PyQt4 import QtCore, QtGui
import engine
import numpy as np


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class myWin(qtView.curveWindow):
    def __init__(self):
        super(myWin, self).__init__()
        self.N=[]
        self.L=[]
        self.P=[]
        self.H=[]
        self.curG = 0

    def setConnections(self):
        super(myWin, self).setConnections()

        clickable1=[self.ui.radio_view,self.ui.radio_deriv]
        clickable2=[self.ui.segment]
        editable =[self.ui.derorder,self.ui.s_mth,self.ui.s_vth,self.ui.sg_fw,self.ui.sg_fo,self.ui.plath,self.ui.lasth]
        for o in clickable1:
                QtCore.QObject.connect(o, QtCore.SIGNAL(_fromUtf8("clicked()")), self.refreshCurve)
        for o in clickable2:
                QtCore.QObject.connect(o, QtCore.SIGNAL(_fromUtf8("clicked()")), self.updateCurve)
        for o in editable:
                QtCore.QObject.connect(o, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.updateCurve)
                QtCore.QObject.connect(o, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), self.updateCurve)
        QtCore.QObject.connect(self.ui.bStat, QtCore.SIGNAL(_fromUtf8("clicked()")), self.doStats)
        QtCore.QObject.connect(self.ui.cIsto, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.refreshIsto)
        QtCore.QObject.connect(self.ui.nBins, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.refreshIsto)

        QtCore.QObject.connect(self.ui.cScatter, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.refreshScatter)
        QtCore.QObject.connect(self.ui.bClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clearAll)
        QtCore.QObject.connect(self.ui.bFreeze, QtCore.SIGNAL(_fromUtf8("clicked()")), self.freezeIsto)
        QtCore.QObject.connect(self.ui.bSSave, QtCore.SIGNAL(_fromUtf8("clicked()")), self.saveStats)
        QtCore.QMetaObject.connectSlotsByName(self)
    def clearAll(self):
        self.exp = experiment.experiment()
        self.refillList()

    def freezeIsto(self):
        self.ui.isto.plot([0,0],[1,1])

    def saveStats(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Filename', './')
        if fname ==None:
            return

        sg_fw =self.ui.sg_fw.value()
        sg_fo =self.ui.sg_fo.value()
        s_mth =self.ui.s_mth.value()
        s_vth =self.ui.s_vth.value()
        plath = self.ui.plath.value()
        lasth = self.ui.lasth.value()

        out_file = open(str(fname),"w")
        out_file.write("# STATS EXPORT\n")

        out_file.write("# {0}:{1}\n".format('WindowSize',sg_fw))
        out_file.write("# {0}:{1}\n".format('SGOrder',sg_fo))
        out_file.write("# {0}:{1}\n".format('DerThreshold',s_mth))
        out_file.write("# {0}:{1}\n".format('MinLength',s_vth))
        out_file.write("# {0}:{1}\n".format('PlateauxLengthThreshold',plath))
        out_file.write("# {0}:{1}\n".format('HeightJumpThreshold',lasth))
        out_file.write("# fname;curveN;L;P;H\n")
        j=0
        for c in self.exp:
            j+=1
            st = c.stats
            if st != None:
                for i in range(len(st['L'])):
                    out_file.write("{0};{1};{2};{3};{4}\n".format(c.filename,j,st['L'][i],st['P'][i],st['H'][i]))

        out_file.close()


    def viewCurve(self,dove = 1,autorange=True):
        isc = self.ui.radio_view.isChecked()
        iss = self.ui.segment.isChecked()

        dove -= 1
        self.ui.grafo.clear()
        p = self.exp[dove][-1]

        sg_fo =self.ui.sg_fo.value()
        derorder = self.ui.derorder.value()
        s_mth =self.ui.s_mth.value()
        s_vth =self.ui.s_vth.value()
        plath = self.ui.plath.value()
        lasth = self.ui.lasth.value()

        ifrom = np.argmax(p.f)
        x = p.z[ifrom:]
        y = p.f[ifrom:]
        ar = None


        sg_fw = int( self.ui.sg_fw.value() * len(x)/100.0)
        if sg_fw % 2 == 0:
            sg_fw+=1

        htmlpre = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:"Ubuntu"; font-size:11pt; font-weight:400; font-style:normal;">\n<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">'
        htmlpost = '</span></p></body></html>'
        details = 'N: {0}'.format(len(p.z))
        


        if isc:
            self.ui.grafo.plot(x,y,pen='k')
            if iss:

                y2 = engine.getSG(y,filtwidth=sg_fw,filtorder=sg_fo,deriv=1)
                yc = y2[int(len(y2)/3):-int(len(y2)/6)]
                mth = np.std(y2) * s_mth
                details = details + ' - mth: {0} - STD[win]: {1} - STD [full]: {2}'.format(mth,np.std(yc),np.std(y2))

                segs = engine.act(x,y,mainth = mth,vth = s_vth,filtwidth = sg_fw,filtorder = sg_fo,plath=plath,lasth=lasth)
                ar = segs[0].x[0]
                i=0
                prevss = segs[0]
                for ss in segs:
                    c = 'b'
                    if ss.plat:
                        if ss.last:
                            i+=1
                        if i%2 == 0:
                            c = 'r'
                        else:
                            c = 'g'
                    else:
                        c = 'b'
                    prevss = ss
                    sx,sy = ss.getPoints()
                    self.ui.grafo.plot(sx,sy,pen=c)
            else:
                y = engine.getSG(y,filtwidth=sg_fw,filtorder=sg_fo,deriv=0)
                self.ui.grafo.plot(x,y,pen='r')
            if autorange:
                self.ui.grafo.autoRange()
                if ar != None:
                    self.ui.grafo.setRange(xRange=(0,ar))
        else:
            y = engine.getSG(y,filtwidth=sg_fw,filtorder=sg_fo,deriv=derorder)
            self.ui.grafo.plot(x,y,pen='b')
            if autorange:
                self.ui.grafo.autoRange()

            yc = y[int(len(y)/3):-int(len(y)/6)]
            mth = np.std(yc) * s_mth

            xx = np.linspace(x[0],x[-1],3)
            yy = np.ones(3)*mth
            self.ui.grafo.plot(xx,yy,pen='r')
        self.ui.labDetails.setText(htmlpre + details + htmlpost)
		
    def doStats(self):
        self.N=[]
        self.L=[]
        self.P=[]
        self.H=[]

        sg_fw_v =self.ui.sg_fw.value()
        sg_fo =self.ui.sg_fo.value()
        derorder = self.ui.derorder.value()
        s_mth =self.ui.s_mth.value()
        s_vth =self.ui.s_vth.value()
        plath = self.ui.plath.value()
        lasth = self.ui.lasth.value()

        QtCore.QCoreApplication.processEvents()
        pmax = len(self.exp)
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtGui.QProgressDialog("Processing curves...", "Cancel stats", 0, pmax);
        i=0
        for c in self.exp:
            QtCore.QCoreApplication.processEvents()
            p = c[-1]
            ifrom = np.argmax(p.f)
            x = p.z[ifrom:]
            y = p.f[ifrom:]
            sg_fw = int( self.ui.sg_fw.value() * len(x)/100.0)
            if sg_fw % 2 == 0:
                sg_fw+=1
            y2 = engine.getSG(y,filtwidth=sg_fw,filtorder=sg_fo,deriv=1)
            yc = y2[int(len(y2)/3):-int(len(y2)/6)]
            mth = np.std(yc) * s_mth

            segs = engine.act(x,y,mainth = mth,vth = s_vth,filtwidth = sg_fw,filtorder = sg_fo,plath=plath,lasth=lasth)

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

            progress.setValue(i)
            i+=1
            if (progress.wasCanceled()):
                break
        progress.setValue(pmax)
        QtGui.QApplication.restoreOverrideCursor()

        self.refreshIsto(9)
        self.refreshScatter(9)

    def refreshIsto(self,indexchanged=0):
        if len(self.ui.isto.listDataItems())>0:
            self.ui.isto.removeItem(self.ui.isto.listDataItems()[-1])
        h = np.array(self.H)
        val1 = [self.L,self.N,h[np.where(h != 0)]]
        y,x = np.histogram(val1[self.ui.cIsto.currentIndex()], bins=self.ui.nBins.value(),normed=True)
        x=(x[1:]+x[0:-1])/2.0

        xx=[]
        yy=[]
        for i in range(len(x)-1):
            xx.append(x[i])
            xx.append(x[i+1])
            yy.append(y[i])
            yy.append(y[i])
        xx.append(x[-1])
        yy.append(y[-1])

        self.ui.isto.plot(xx, yy, fillLevel=0, brush=(0, 0, 255, 80),pen='b')

        if indexchanged != 9:
            self.ui.isto.autoRange()

    def refreshScatter(self,indexchanged=0):
        if len(self.ui.scatter.listDataItems())>0:
            self.ui.scatter.removeItem(self.ui.scatter.listDataItems()[-1])
        y1 = [self.L,self.H,self.H]
        x1 = [self.P,self.P,self.L]

        self.ui.scatter.plot(x1[self.ui.cScatter.currentIndex()], y1[self.ui.cScatter.currentIndex()], pen=None, symbol='o',symbolSize=5)

        if indexchanged != 9:
            self.ui.scatter.autoRange()

        #plt2.plot(vals, y, pen=None, symbol='o', symbolSize=5)
        #plt2.plot(vals, y, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName( 'qtView' )
    canale = myWin()
    canale.show()
    QtCore.QObject.connect( app, QtCore.SIGNAL( 'lastWindowClosed()' ), app, QtCore.SLOT( 'quit()' ) )
    sys.exit(app.exec_())
