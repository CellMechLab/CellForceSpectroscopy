from PyQt5 import QtCore, QtGui, QtWidgets

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


class curveWindow ( QtWidgets.QMainWindow ):
    iter = 0
    prev = 0
    cRosso = QtGui.QColor(255,0,0)
    cVerde = QtGui.QColor(50,255,50)
    cNero = QtGui.QColor(0,0,0)
    def __init__ ( self, parent = None ):
        QtWidgets.QMainWindow.__init__( self, parent )
        self.setWindowTitle( 'qt-ONE-View' )
        self.ui = view.Ui_facewindow()
        self.ui.setupUi( self )
        self.setConnections()
        self.exp = experiment.experiment()
        self.curve = curve.curve()
        self.noupdate = False
        self.generalsegmentation = segmentation.segmentation()
        self.populateGsegment()

    def populateGsegment(self):
        self.generalsegmentation.slope = self.ui.sg_mm.value()
        self.generalsegmentation.mainth = self.ui.s_mth.value()
        self.generalsegmentation.window = self.ui.sg_fw.value()
        self.generalsegmentation.minlen = self.ui.s_vth.value()
        self.generalsegmentation.zmin = self.ui.plath.value()
        self.generalsegmentation.deltaF = self.ui.lasth.value()
        self.generalsegmentation.trorder = self.ui.derorder.value()

    def getCurrentSeg(self):
        s = segmentation.segmentation()
        s.slope = self.ui.sg_mm.value()
        s.mainth = self.ui.s_mth.value()
        s.window = self.ui.sg_fw.value()
        s.minlen = self.ui.s_vth.value()
        s.zmin = self.ui.plath.value()
        s.deltaF = self.ui.lasth.value()
        s.trorder = self.ui.derorder.value()
        return s

    def setCurrentSeg(self,s):
        self.noupdate = True
        s.slope = self.ui.sg_mm.setValue(s.slope)
        self.ui.s_mth.setValue(s.mainth)
        self.ui.sg_fw.setValue(s.window)
        self.ui.s_vth.setValue(s.minlen)
        self.ui.plath.setValue(s.zmin)
        self.ui.lasth.setValue(s.deltaF)
        self.ui.derorder.setValue(s.trorder)
        self.noupdate = False

    def chCustom(self):
        state = self.ui.cscope.isChecked()
        if state is True:
            self.ui.cscope.setText('Custom')
            self.ui.cscope.setStyleSheet('color: red;')
            self.curve.custom = True
            self.curve.customSegmentation = self.getCurrentSeg()
        else:
            self.ui.cscope.setText('General')
            self.ui.cscope.setStyleSheet('')
            self.curve.custom = False

    def statSave(self):

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Segmenting curves...", "Cancel operation", 0, len(self.exp))

        sgen = self.generalsegmentation

        for i in range(len(self.exp)):
            QtCore.QCoreApplication.processEvents()
            if self.exp[i].custom is True and self.exp[i].customSegmentation is not None:
                self.exp[i][-1].traits = self.exp[i].customSegmentation.run(self.exp[i][-1])
                self.exp[i][-1].segmentation = self.exp[i].customSegmentation
            else:
                self.exp[i][-1].traits = sgen.run(self.exp[i][-1])
                self.exp[i][-1].segmentation = sgen
            progress.setValue(i)
            if progress.wasCanceled():
                QtWidgets.QApplication.restoreOverrideCursor()
                return
        progress.setValue(len(self.exp))
        QtWidgets.QApplication.restoreOverrideCursor()

        fname = QtWidgets.QFileDialog.getSaveFileName  (self, 'Select the file for saving stats',filter="Text file (*.csv *.txt)")
        if fname is None or fname is False:
            return

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Calculating stats...", "Cancel operation", 0, len(self.exp))

        cvfile = open(str(fname[0]),"w")
        import os.path
        pieces = os.path.splitext(str(fname[0]))
        trfile = open(pieces[0]+'_traits'+pieces[1],"w")
        import uuid
        gid = uuid.uuid4()
        cvfile.write("# Curve stats {0}\n".format(gid))
        trfile.write("# Trait stats {0}\n".format(gid))
        names = ['Slope threshold','Main der Threshold','Filtering window','Min length','Min initial position','Min step for breaking trait','Order']
        values = [sgen.slope,sgen.mainth,sgen.window,sgen.minlen,sgen.zmin,sgen.deltaF,sgen.trorder]
        for f in [cvfile,trfile]:
            f.write("# Global segmentation parameters\n")
            for i in range(len(values)):
                f.write("# {0}:{1}\n".format(names[i],values[i]))
        cvfile.write("#ID;FNAME;ADHESION [pN];AREA [zJ];NTRAITS;NJUMPS;NPLATEAUX\n")
        trfile.write("#ID;CURVEID;FNAME;LENGTH [nm];POSITION [nm];STEP [pN]\n")
        for i in range(len(self.exp)):
            nj = 0
            np = 0
            QtCore.QCoreApplication.processEvents()
            for j in range(1,len(self.exp[i][-1].traits)):
                tr = self.exp[i][-1].traits[j]
                if tr.accept:
                    trfile.write("{0};{1};{2};".format(j,i,self.exp[i].basename))
                    if tr.pj == 'P':
                        np += 1
                    else:
                        nj += 1
                    trfile.write("{0};{1};{2}\n".format(tr.alen(),min(tr.x),tr-self.exp[i][-1].traits[j-1]))

            cvfile.write("{0};{1};{2};{3};{4};{5};{6}\n".format(i,self.exp[i].basename,self.exp[i][-1].getAdhesion(),self.exp[i][-1].getArea(),len(self.exp[i][-1].traits),nj,np))
            progress.setValue(i)
            if progress.wasCanceled():
                QtWidgets.QApplication.restoreOverrideCursor()
                cvfile.close()
                trfile.close()
                return

        cvfile.close()
        trfile.close()

        progress.setValue(len(self.exp))
        QtWidgets.QApplication.restoreOverrideCursor()

    def addFile(self, fname = None):
        if fname is None or fname is False:
            fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file', './')
        self.curve.open(str(fname[0]))
        self.refillList()
        self.viewCurve()

    def resetAll(self):
        self.exp = experiment.experiment()
        self.curve = curve.curve()
        self.ui.mainlist.clear()
        self.ui.pjlist.clear()
        self.ui.grafo.clear()
        self.noupdate = False
        self.generalsegmentation = segmentation.segmentation()
        self.populateGsegment()

    def addFiles(self,fnames=None):
        if fnames is None or fnames is False:
            q = QtWidgets.QFileDialog()
            q.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
            q.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            if ( q.exec() == 1 ):
                fnames = q.selectedFiles()
            else:
                return
            #fnames = QtWidgets.QFileDialog.getOpenFileNames()[0]
        QtCore.QCoreApplication.processEvents()
        pmax = len(fnames)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Opening files...", "Cancel opening", 0, pmax)
        i=0
        for fname in fnames:
            QtCore.QCoreApplication.processEvents()
            self.exp.addFiles([str(fname)])
            progress.setValue(i)
            i=i+1
            if (progress.wasCanceled()):
                break
        progress.setValue(pmax)
        QtWidgets.QApplication.restoreOverrideCursor()

        self.fileList()

    def addDir(self,dirname=None):
        if dirname is None or dirname is False:
            dirname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a directory', './')
            if not os.path.isdir(dirname):
                return
        QtCore.QCoreApplication.processEvents()
        pmax = len(os.listdir(dirname))

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Opening files...", "Cancel opening", 0, pmax);
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
        QtWidgets.QApplication.restoreOverrideCursor()
        self.fileList()
    
    def fileList(self):
        self.ui.mainlist.clear()
        for c in self.exp:
            self.ui.mainlist.addItem(c.basename)
        self.ui.mainlist.setCurrentRow(0)
        
    def refillList(self,remainThere = False):
        if self.noupdate is True:
            return

        s = self.getCurrentSeg()
        if self.curve.custom is True:
            self.curve.customSegmentation = s
        else:
            self.generalsegmentation = s

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        if len(self.curve)>0:
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
        QtWidgets.QApplication.restoreOverrideCursor()
        return True

    def changeCurve(self,row):
        self.curve = self.exp[row]

        if self.curve.custom is True:
            self.ui.cscope.setChecked(True)
            self.setCurrentSeg(self.curve.customSegmentation)
        else:
            self.ui.cscope.setChecked(False)
            self.setCurrentSeg(self.generalsegmentation)
        self.chCustom()
        self.refillList()
        self.viewCurve()
        
    def updateCurve(self):
        self.sender().setStyleSheet('')
        self.refillList(remainThere=True)
        self.viewCurve(autorange=False)

    def refreshCurve(self):
        self.sender().setStyleSheet('')
        if self.curve.custom is True:
            self.setCurrentSeg(self.curve.customSegmentation)

        self.refillList()
        self.viewCurve(autorange=True)

    def refreshPJ(self,where):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
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
        QtWidgets.QApplication.restoreOverrideCursor()
        return

    def reddish(self,val):
        if self.noupdate is True:
            return
        self.sender().setStyleSheet('color:red')

    def setConnections(self):
        
        clickable1=[self.ui.radio_view,self.ui.radio_deriv,self.ui.radio_smooth]
        editable =[self.ui.derorder,self.ui.s_mth,self.ui.s_vth,self.ui.sg_fw,self.ui.sg_mm,self.ui.plath,self.ui.lasth]
        for o in clickable1:
            o.clicked.connect(self.refreshCurve)
        for o in editable:
            o.editingFinished.connect(self.updateCurve)
            o.valueChanged.connect(self.reddish)

        self.ui.cscope.clicked.connect(self.chCustom)

        self.ui.bAddFile.clicked.connect(self.addFile)
        self.ui.bAddFiles.clicked.connect(self.addFiles)
        self.ui.bAddDir.clicked.connect(self.addDir)

        self.ui.bReset.clicked.connect(self.resetAll)
        self.ui.bDoSave.clicked.connect(self.statSave)

        self.ui.pjlist.currentRowChanged.connect(self.refreshPJ)
        self.ui.mainlist.currentRowChanged.connect(self.changeCurve)
        
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def viewCurve(self,autorange=True):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        isc = self.ui.radio_view.isChecked()
        ism = self.ui.radio_smooth.isChecked()
        
        self.ui.grafo.clear()
        if len(self.curve)>0:
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
        QtWidgets.QApplication.restoreOverrideCursor()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName( 'qt-ONE-View' )
    canale = curveWindow()
    canale.show()
    #QtCore.QObject.connect( app, QtCore.SIGNAL( 'lastWindowClosed()' ), app, QtCore.SLOT( 'quit()' ) )
    sys.exit(app.exec_())
