from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

import sys,os
import pyqtgraph as pg
import canale_view as view
import segmentation
from sifork import curve
from sifork import experiment
import numpy as np
import savitzky_golay as sg

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


htmlpre = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:"Ubuntu"; font-size:11pt; font-weight:400; font-style:normal;">\n<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">'
htmlpost = '</span></p></body></html>'


class curveWindow ( QtGui.QMainWindow ):
    iter = 0
    prev = 0
    cRosso = QtGui.QColor(255,0,0)
    cVerde = QtGui.QColor(50,255,50)
    cNero = QtGui.QColor(0,0,0)
    def __init__ ( self, parent = None ):
        QtGui.QMainWindow.__init__( self, parent )
        self.setWindowTitle( 'qt-ONE-View' )
        self.ui = view.Ui_facewindow()
        self.ui.setupUi( self )
        self.setConnections()
        self.exp = experiment.experiment()
        self.curve = curve.curve()

    def statSave(self):

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtGui.QProgressDialog("Segmenting curves...", "Cancel operation", 0, len(self.exp))

        s = segmentation.segmentation()
        s.slope =self.ui.sg_mm.value()
        s.mainth =self.ui.s_mth.value()
        s.window =self.ui.sg_fw.value()
        s.minlen =self.ui.s_vth.value()
        s.zmin = self.ui.plath.value()
        s.deltaF = self.ui.lasth.value()
        s.trorder = self.ui.derorder.value()

        for i in range(len(self.exp)):
            QtCore.QCoreApplication.processEvents()
            self.exp[i][-1].traits = s.run(self.exp[i][-1])
            self.exp[i][-1].segmentation = s
            progress.setValue(i)
            if progress.wasCanceled():
                QtGui.QApplication.restoreOverrideCursor()
                return
        progress.setValue(len(self.exp))
        QtGui.QApplication.restoreOverrideCursor()

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtGui.QProgressDialog("Calculating stats...", "Cancel operation", 0, len(self.exp))
        for i in range(len(self.exp)):
            QtCore.QCoreApplication.processEvents()
            #self.exp[i][-1].traits = s.run(self.exp[i][-1])
            progress.setValue(i)
            if progress.wasCanceled():
                QtGui.QApplication.restoreOverrideCursor()
                return
        progress.setValue(len(self.exp))
        QtGui.QApplication.restoreOverrideCursor()


    def addFile(self, fname = None):
        if fname == None:
            fname = QtGui.QFileDialog.getOpenFileName(self, 'Select file', './')
        self.curve.open(str(fname))
        self.refillList()
        self.viewCurve()

    def resetAll(self):
        self.exp = experiment.experiment()
        self.curve = curve.curve()
        self.ui.mainlist.clear()
        self.ui.pjlist.clear()
        self.ui.grafo.clear()

    def addFiles(self,fnames=None):
        if fnames == None:
            fnames = QtGui.QFileDialog.getOpenFileNames(self, 'Select files', './')
        QtCore.QCoreApplication.processEvents()
        pmax = len(fnames)

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtGui.QProgressDialog("Opening files...", "Cancel opening", 0, pmax)
        i=0
        for fname in fnames:
            QtCore.QCoreApplication.processEvents()
            self.exp.addFiles([str(fname)])
            progress.setValue(i)
            i=i+1
            if (progress.wasCanceled()):
                break
        progress.setValue(pmax)
        QtGui.QApplication.restoreOverrideCursor()

        self.fileList()

    def addDir(self,dirname=None):
        if dirname == None:
            dirname = QtGui.QFileDialog.getExistingDirectory(self, 'Select a directory', './')
            if not os.path.isdir(dirname):
                return
        QtCore.QCoreApplication.processEvents()
        pmax = len(os.listdir(dirname))

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtGui.QProgressDialog("Opening files...", "Cancel opening", 0, pmax);
        i=0
        for fnamealone in os.listdir(dirname):
            #if i % 100 == 0:
            QtCore.QCoreApplication.processEvents()
            fname = os.path.join(str(dirname), fnamealone)
            self.exp.addFiles([str(fname)])
            progress.setValue(i)
            i=i+1
            if (progress.wasCanceled()):
                break
        progress.setValue(pmax)
        QtGui.QApplication.restoreOverrideCursor()
        self.fileList()
    
    def fileList(self):
        self.ui.mainlist.clear()
        for c in self.exp:
            self.ui.mainlist.addItem(c.basename)
        self.ui.mainlist.setCurrentRow(0)
        
    def refillList(self,remainThere = False):
        s = segmentation.segmentation()
        s.slope =self.ui.sg_mm.value()
        s.mainth =self.ui.s_mth.value()
        s.window =self.ui.sg_fw.value()
        s.minlen =self.ui.s_vth.value()
        s.zmin = self.ui.plath.value()
        s.deltaF = self.ui.lasth.value()
        s.trorder = self.ui.derorder.value()

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.curve[-1].traits = s.run(self.curve[-1])
        self.curve[-1].segmentation = s

        # set here the refresh of the segments list
        # if remainThere, after filling, go to the last segment
        
        self.ui.lcd_N.display(len(self.curve[-1].traits))      
        
        self.ui.pjlist.clear()
        nump = 0
        numj = 0
        numb = 0
        for i in range(len(self.curve[-1].traits)):
            t = self.curve[-1].traits[i]
            if t.accept:
                if t.slope() < s.slope:
                    t.pj='P'
                    nump+=1
                else:
                    t.pj='J'
                    numj+=1
            else:
                numb+=1
            self.ui.pjlist.addItem('{0}'.format(i+1))

        self.ui.lcd_Np.display(nump)
        self.ui.lcd_Nj.display(numj)
        self.ui.lcd_Nblue.display(numb)
        QtGui.QApplication.restoreOverrideCursor()
        return True
    def changeCurve(self,row):
        self.curve = self.exp[row]
        self.refillList()
        self.viewCurve()
        
    def updateCurve(self):
        self.refillList(remainThere=True)
        self.viewCurve(autorange=False)

    def refreshCurve(self):
        self.refillList()
        self.viewCurve(autorange=True)

    def refreshPJ(self,where):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        w = self.ui.pjlist.currentRow()
        
        tr = self.curve[-1].traits[w]
        
        left = min(tr.x)
        right = max(tr.x)
        
        self.ui.riga.setRegion((left,right))
        
        self.ui.lcd_Tposition.display(left)
        self.ui.lcd_Tlength.display(tr.alen())
        if w == 0:
            self.ui.lcd_Tstep.display(0)
        else:
            self.ui.lcd_Tstep.display(tr-self.curve[-1].traits[w-1])
        self.ui.lcd_Tslope.display(tr.slope())
        if tr.pj == 'P':
            self.ui.pj_p.setChecked(True)
        else:
            self.ui.pj_j.setChecked(True)
            
        if tr.accept:
            self.ui.fil_io.setValue(1)
        else:
            self.ui.fil_io.setValue(0)
        QtGui.QApplication.restoreOverrideCursor()
        return
        
    def setConnections(self):
        
        clickable1=[self.ui.radio_view,self.ui.radio_deriv,self.ui.radio_smooth]
        editable =[self.ui.derorder,self.ui.s_mth,self.ui.s_vth,self.ui.sg_fw,self.ui.sg_mm,self.ui.plath,self.ui.lasth]
        for o in clickable1:
                QtCore.QObject.connect(o, QtCore.SIGNAL(_fromUtf8("clicked()")), self.refreshCurve)
        for o in editable:
            QtCore.QObject.connect(o, QtCore.SIGNAL(_fromUtf8("editingFinished()")), self.updateCurve)

        QtCore.QObject.connect(self.ui.bAddFile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.addFile)
        QtCore.QObject.connect(self.ui.bAddFiles, QtCore.SIGNAL(_fromUtf8("clicked()")), self.addFiles)
        QtCore.QObject.connect(self.ui.bAddDir, QtCore.SIGNAL(_fromUtf8("clicked()")), self.addDir)
        QtCore.QObject.connect(self.ui.bReset, QtCore.SIGNAL(_fromUtf8("clicked()")), self.resetAll)
        QtCore.QObject.connect(self.ui.bDoSave, QtCore.SIGNAL(_fromUtf8("clicked()")), self.statSave)

        QtCore.QObject.connect(self.ui.pjlist, QtCore.SIGNAL(_fromUtf8("currentRowChanged(int)")), self.refreshPJ)
        QtCore.QObject.connect(self.ui.mainlist, QtCore.SIGNAL(_fromUtf8("currentRowChanged(int)")), self.changeCurve)
        
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def viewCurve(self,autorange=True):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        isc = self.ui.radio_view.isChecked()
        ism = self.ui.radio_smooth.isChecked()
        
        self.ui.grafo.clear()
        p = self.curve[-1]

        #ifrom = np.argmax(p.f)
        x = p.z#[ifrom:]
        y = p.f#[ifrom:]
        ar = None

        htmlpre = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:"Ubuntu"; font-size:11pt; font-weight:400; font-style:normal;">\n<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">'
        htmlpost = '</span></p></body></html>'
        details = 'N: {0}'.format(len(p.z))
        
        if isc:
            self.ui.grafo.plot(x,y,pen='k')
            #y2 = sg.getSG(y,filtwidth=self.curve[-1].segmentation.abswin,deriv=0)
            
            #self.ui.grafo.plot(x,y2,pen='b')
            

            ar = self.curve[-1].traits[0].x[0]
            i=0
            prevss = self.curve[-1].traits[0]
            for ss in self.curve[-1].traits:
                c = 'b'
                if ss.accept:
                    if ss.last:
                        i+=1
                    if i%2 == 0:
                        c = 'r'
                    else:
                        c = 'g'
                    if ss.pj=='J':
                        c = 'y'
                else:
                    c = 'b'
                prevss = ss
                tro = self.ui.derorder.value()
                if tro==1:
                    sx,sy = ss.getPoints(mode='lin')
                else:
                    sx,sy = ss.getPoints(mode='poly',polyorder=tro)
                self.ui.grafo.plot(sx,sy,pen=c)
                self.ui.riga = pg.LinearRegionItem(movable=False)
                self.ui.grafo.addItem(self.ui.riga)
            if autorange:
                self.ui.grafo.autoRange()
                if ar != None:
                    self.ui.grafo.setRange(xRange=(0,ar))
        elif ism:
            self.ui.grafo.plot(x,y,pen='k')
            y2 = sg.getSG(y,filtwidth=self.curve[-1].segmentation.abswin,deriv=0)
            self.ui.grafo.plot(x,y2,pen='b')
            if autorange:
                self.ui.grafo.autoRange()

        else:
            
            y = sg.getSG(y,filtwidth=self.curve[-1].segmentation.abswin)
            self.ui.grafo.plot(x,y,pen='b')
            if autorange:
                self.ui.grafo.autoRange()

            xx = np.linspace(x[0],x[-1],3)
            yy = np.ones(3)*self.curve[-1].segmentation.absth
            self.ui.grafo.plot(xx,yy,pen='r')
        self.ui.labDetails.setText(htmlpre + details + htmlpost)
        self.ui.labFilename.setText(self.curve.filename)
        QtGui.QApplication.restoreOverrideCursor()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName( 'qt-ONE-View' )
    canale = curveWindow()
    canale.show()
    QtCore.QObject.connect( app, QtCore.SIGNAL( 'lastWindowClosed()' ), app, QtCore.SLOT( 'quit()' ) )
    sys.exit(app.exec_())
