from PyQt5 import QtCore, QtGui, QtWidgets

_fromUtf8 = lambda s: s

import sys,os
import pyqtgraph as pg
import Ui_canale_view as view
import segmentation
from sifork import curve
from sifork import experiment
import numpy as np
from scipy.optimize import curve_fit
from outliers import smirnov_grubbs as grubbs

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

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


htmlpre = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:"Ubuntu"; font-size:11pt; font-weight:400; font-style:normal;">\n<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">'
htmlpost = '</span></p></body></html>'


class CurveWindow (QtWidgets.QMainWindow):
    iter = 0
    prev = 0
    cRosso = QtGui.QColor(255,0,0)
    cVerde = QtGui.QColor(50,255,50)
    cNero = QtGui.QColor(0,0,0)

    def __init__ ( self, parent = None ):
        QtWidgets.QMainWindow.__init__( self, parent )
        self.setWindowTitle( 'qt-ONE-View' )

        self.color_jump1 = 'r'
        self.color_jump2 = 'y'
        self.color_plateaux1 = 'b'
        self.color_plateaux2 = 'g'
        self.color_bad = QtGui.QColor('gray') 

        self.ui = view.Ui_facewindow()
        self.ui.setupUi( self )
        self.ui.splitter.setSizes([820, 410])
        self.ui.splitter_2.setSizes([328,240])
        self.ui.splitter_2.setStretchFactor(1,0)
        self.setConnections()
        self.exp = experiment.experiment()
        self.curve = curve.curve()
        self.noRed = [self.ui.arBlue,self.ui.arGreen]
        self.noupdate = False
        self.labels=[]
        self.generalsegmentation = segmentation.segmentation()
        self.populateGsegment()
        self.prevStat = None
        self.ui.stat.addLegend()

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

    def redoStat(self):
        self.segmentAll()
        self.dostat()

    def segmentAll(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Segmenting curves...", "Cancel operation", 0, len(self.exp))
        sgen = self.generalsegmentation
        for i in range(len(self.exp)):
            QtCore.QCoreApplication.processEvents()
            if self.exp[i].custom is True and self.exp[i].customSegmentation is not None:
                self.exp[i]['up'].traits = self.exp[i].customSegmentation.run(self.exp[i]['up'])
                self.exp[i]['up'].segmentation = self.exp[i].customSegmentation
            else:
                self.exp[i]['up'].traits = sgen.run(self.exp[i]['up'])
                self.exp[i]['up'].segmentation = sgen
            progress.setValue(i)
            if progress.wasCanceled():
                QtWidgets.QApplication.restoreOverrideCursor()
                return
        progress.setValue(len(self.exp))
        QtWidgets.QApplication.restoreOverrideCursor()
        self.exp.segmented = True

    def statSave(self):
        #XXX
        self.segmentAll()
        sgen = self.generalsegmentation
        fname = QtWidgets.QFileDialog.getSaveFileName  (self, 'Select the file for saving stats',filter="Text file (*.csv *.txt)")
        if fname is None or fname is False:
            return

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Calculating stats and saving...", "Cancel operation", 0, len(self.exp))

        cvfile = open(str(fname[0]),"w")
        import os.path
        pieces = os.path.splitext(str(fname[0]))
        trfile = open(pieces[0]+'_traits'+pieces[1],"w")
        import uuid
        gid = uuid.uuid4()
        cvfile.write("# Curve stats {0}\n".format(gid))
        trfile.write("# Trait stats {0}\n".format(gid))
        names = ['Slope threshold','Main der Threshold','Filtering window','Min length','Min initial position','Min step for breaking trait','Order','Area reflatten']
        values = [sgen.slope,sgen.mainth,sgen.window,sgen.minlen,sgen.zmin,sgen.deltaF,sgen.trorder,]
        for f in [cvfile,trfile]:
            f.write("# Global segmentation parameters\n")
            for i in range(len(values)):
                f.write("# {0}:{1}\n".format(names[i],values[i]))
            f.write('# Additional parameters\n')
            f.write("# {0}:{1}\n".format('Jump mode','Blue' if (self.ui.arBlue.isChecked() is True) else 'Green'))
            f.write("# {0}:{1}\n".format('JArea threshold',self.ui.str_lim.text()))
        curveStats = ['Family','speed first [nm/s]','speed last [nm/2]','contact time [s]','setpoint [pN]','ADHESION [pN]','Jump AREA [aJ]','DETACH-X [nm]','DETACH-F [pN]','X-NearFar [nm]','AREA [aJ]','STRETCH AREA [aJ]','NTRAITS','NJUMPS','NPLATEAUX'] #,'Max Step [pN]']
        cvfile.write("#ID;FNAME")
        for stat in curveStats:
            cvfile.write(";{}".format(stat))
        cvfile.write("\n")
        trStats = ['LENGTH [nm]','POSITION [nm]','STEP [pN]','SLOPE [pN/nm]']
        trfile.write("#ID;CURVEID;FNAME")
        for stat in trStats:
            trfile.write(";{}".format(stat))
        trfile.write("\n")
        for i in range(len(self.exp)):
            cv = self.exp[i]
            cvfile.write("{0};{1}".format(i,cv.basename))
            cline=[]
            cline.append(cv.family)
            try:
                cline.append(cv['down'].speed)
            except:
                cline.append(0)
            try:
                cline.append(cv['up'].speed)
            except:
                cline.append(0)
            try:
                cline.append(cv[1].duration)
            except:
                cline.append(0)
            try:
                cline.append(cv['down'].setpoint)
            except:
                cline.append(0)
            try:
                cline.append(cv['up'].getAdhesion())
            except:
                cline.append(0)
            try:
                cline.append(1e-3**cv.getStretchArea(self.ui.arBlue.isChecked()))
            except:
                cline.append(0)
            try:
                cline.append(cv.getDetachPoint())
            except:
                cline.append(0)
            try:
                cline.append(cv.getDetachForce())
            except:
                cline.append(0)
            try:
                cline.append(cv.getNearFarPoint()[0])
            except:
                cline.append(0)
            try:
                reflatten = self.ui.reflatten.isChecked()
                poly = self.ui.derorder.value()
                area = cv['up'].getArea( reflatten=reflatten,polyorder=poly)
                cline.append(1.0e-3*area)
            except:
                cline.append(0)
            try:
                cline.append(1.0e-3*cv['up'].getStretchTo(float(self.ui.str_lim.value())))
            except:
                cline.append(0)
            try:
                nump,numj,numb = cv['up'].getNumbers()
            except:
                nump,numj,numb = 0,0,0
            cline.append(nump+numj+numb)
            cline.append(numj)
            cline.append(nump)
            #cline.append(cv[-1].getMaxStep(isFiltered,[self.ui.lim_min_xtrait.value() ,self.ui.lim_max_xtrait.value() ],[self.ui.lim_min_length.value(),self.ui.lim_max_length.value()]))
            for number in cline:
                cvfile.write(";{}".format(number))
            cvfile.write("\n")
            QtCore.QCoreApplication.processEvents()
            try:
                if len(cv['up'].traits)>0:
                    pret = cv['up'].traits[0]
                for j in range(1,len(cv['up'].traits)):
                    tr = cv['up'].traits[j]
                    if tr.accept:
                        trfile.write("{0};{1};{2}".format(j,i,cv.basename))
                        tline = []
                        tline.append(tr.alen())
                        tline.append(min(tr.x))
                        tline.append(tr-pret)
                        tline.append(tr.slope(angle=False))
                        pret = tr
                        for number in tline:
                            trfile.write(";{}".format(number))
                        trfile.write("\n")
            except:
                pass
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
        self.labels=[]
        self.ui.cvTree.reset()
        #self.ui.leg_label.setText('')
        self.ui.cbar.setMaximum(0)
        self.ui.cbar.setValue(0)
        self.ui.pjbar.setMaximum(1)
        self.ui.pjbar.setValue(1)
        self.ui.grafo.clear()
        self.noupdate = False
        newMax = 1
        self.ui.cFamilyLoad.setMaximum(newMax )
        self.ui.cFamily.setMaximum(newMax)
        self.ui.cNumFam.setText(str(newMax))
        self.ui.cFamilyLoad.setValue(newMax)
        self.generalsegmentation = segmentation.segmentation()
        self.populateGsegment()

    def addFiles(self,fnames=None):
        if fnames is None or fnames is False:
            qDialog = QtWidgets.QFileDialog()
            qDialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
            qDialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            r = qDialog.exec()
            if r == 1:
                fnames = qDialog.selectedFiles()
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
            self.exp.addFiles([str(fname)],family = self.getFamily())
            progress.setValue(i)
            i=i+1
            if (progress.wasCanceled()):
                break
        progress.setValue(pmax)
        QtWidgets.QApplication.restoreOverrideCursor()

        self.fileList()

    def getFamily(self):
        theFamily = 1
        if self.ui.famGroup.isChecked() is True:
            theFamily = int(self.ui.cFamilyLoad.value())
        return theFamily

    def addDir(self,dirname=None):
        if dirname is None or dirname is False:
            dirname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a directory', './')
            if not os.path.isdir(dirname):
                return
        QtCore.QCoreApplication.processEvents()
        pmax = len(os.listdir(dirname))

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Opening files...", "Cancel opening", 0, pmax)
        i=0
        for fnamealone in os.listdir(dirname):
            #if i % 100 == 0:
            QtCore.QCoreApplication.processEvents()
            fname = os.path.join(str(dirname), fnamealone)

            self.exp.addFiles([str(fname)],family = self.getFamily())
            progress.setValue(i)
            i=i+1
            if (progress.wasCanceled()):
                break
        progress.setValue(pmax)
        QtWidgets.QApplication.restoreOverrideCursor()
        self.fileList()

    def fileList(self):
        self.ui.cbar.setMaximum(len(self.exp)-1)
        self.ui.cbar.setTickInterval(int(len(self.exp)/11))
        self.ui.cbar.setPageStep(int(len(self.exp)/21))
        self.ui.cbar.setValue(len(self.exp)-1)

    def rescale(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Rescaling curves...", "Cancel operation", 0, len(self.exp))
        if self.exp.segmented is False:
            self.segmentAll()
        for i in range(len(self.exp)):
            QtCore.QCoreApplication.processEvents()
            if self.exp[i].recalibrated is False:
                self.exp[i].recalibrateContactRegion()
            if progress.wasCanceled():
                QtWidgets.QApplication.restoreOverrideCursor()
                return
        progress.setValue(len(self.exp))
        QtWidgets.QApplication.restoreOverrideCursor()
        self.viewCurve(autorange=True)

    def flatten(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Flattening curves...", "Cancel operation", 0, len(self.exp))
        if self.exp.segmented is False:
            self.segmentAll()
        for i in range(len(self.exp)):
            QtCore.QCoreApplication.processEvents()
            if self.exp[i].flattened is False:
                self.exp[i].flatten()
            if progress.wasCanceled():
                QtWidgets.QApplication.restoreOverrideCursor()
                return
        progress.setValue(len(self.exp))
        QtWidgets.QApplication.restoreOverrideCursor()
        self.viewCurve(autorange=True)

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
            self.curve['up'].traits = s.run(self.curve['up'])
            self.curve['up'].segmentation = s

            # set here the refresh of the segments list
            # if remainThere, after filling, go to the last segment

            lab = str(len(self.curve['up'].traits))
            self.ui.lab_N.setText('{:}'.format(lab))

            self.ui.pjbar.setMaximum(1)
            self.ui.pjbar.setValue(1)
            nump = 0
            numj = 0
            numb = 0
            self.ui.pjbar.setMaximum(len(self.curve['up'].traits))
            nump,numj,numb = self.curve['up'].getNumbers()
            self.ui.lab_Np.setText('{:}'.format(nump))
            self.ui.lab_Nj.setText('{:}'.format(numj))
            self.ui.lab_Nblue.setText('{:}'.format(numb))
            self.ui.cFamily.setValue(self.curve.family)
            self.ui.lcd_hieght.setText('{:.2g} pN'.format(self.curve['up'].getMaxStep(self.ui.filters_group.isChecked(),[self.ui.lim_min_xtrait.value() ,self.ui.lim_max_xtrait.value() ],[self.ui.lim_min_length.value(),self.ui.lim_max_length.value()])))
            #XXX
            reflatten = self.ui.reflatten.isChecked()
            polyorder = self.ui.derorder.value()
            area = self.curve['up'].getArea(reflatten,polyorder)
            self.ui.lcd_Area.setText('{:.2g} aJ'.format(1.0e-3*area))
            self.ui.lcd_JArea.setText('{:.2g} aJ'.format(1.0e-3*self.curve['up'].getStretchArea(self.ui.arBlue.isChecked())))
            self.ui.lcd_strA.setText('{:.2g} aJ'.format(1.0e-3*self.curve['up'].getStretchTo(float(self.ui.str_lim.value()))))
            dp = self.curve.getDetachPoint()
            if dp is None:
                self.ui.lcd_detX.setText('Err')
            else:
                self.ui.lcd_detX.setText('{:.2g} nm'.format(dp))
            df = self.curve.getDetachForce()
            if df is None:
                self.ui.lcd_detF.setText('Err')
            else:
                self.ui.lcd_detF.setText('{:.2g} pN'.format(df))
        QtWidgets.QApplication.restoreOverrideCursor()
        return True

    def popout(self):
        icurve = int(self.ui.cnumb.text())-1
        del(self.exp[icurve])
        self.fileList()

    def changeCurve(self,row):
        self.curve = self.exp[row]
        self.ui.cnumb.setText(str(row+1))

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
        if self.sender() not in self.noRed:
            self.sender().setStyleSheet('')
        self.refillList(remainThere=True)
        self.viewCurve(autorange=False)

    def refreshCurve(self):
        if self.sender() not in self.noRed:
            self.sender().setStyleSheet('')
        if self.curve.custom is True:
            self.setCurrentSeg(self.curve.customSegmentation)

        self.refillList()
        self.viewCurve(autorange=True)

    def refreshPJ(self,w):
        #w = self.ui.pjbar.value()-1
        self.ui.pjnumb.setText(str(w+1))
        if len(self.curve['up'].traits)<=w or w == -1:
            return
        tr = self.curve['up'].traits[w]
        #QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        left = min(tr.x)
        right = max(tr.x)
        try:
            self.ui.riga.setRegion((left,right))
        except:
            pass
        self.ui.lab_Tposition.setText('{:.2f}'.format(left))
        self.ui.lab_Tlength.setText('{:.2f}'.format(tr.alen()))
        if w == 0:
            self.ui.lab_Tstep.setText('0')
        else:
            self.ui.lab_Tstep.setText('{:.2f}'.format(tr-self.curve['up'].traits[w-1]))
        self.ui.lab_Tslope.setText('{:.2f}'.format(tr.slope()))
        if tr.pj == 'P':
            self.ui.lab_pj.setText('Plateau')
        else:
            self.ui.lab_pj.setText('Jump')

        if tr.accept:
            self.ui.fil_io.setValue(1)
        else:
            self.ui.fil_io.setValue(0)
        #QtWidgets.QApplication.restoreOverrideCursor()
        return

    def reddish(self,val):
        if self.noupdate is True:
            return
        self.sender().setStyleSheet('color:red')

    def chStat(self):
        self.ui.lim_custom.setChecked(False)
        self.dostat()

    def clearLegend(self):
        leg = self.ui.stat.plotItem.legend
        for sample, label in leg.items:
            #leg.items.remove( (sample, label) )    # remove from itemlist
            leg.layout.removeItem(sample)          # remove from layout
            sample.close()                          # remove from drawing
            leg.layout.removeItem(label)
            label.close()
        leg.items=[]
        leg.updateSize()

    def dostat(self):
        self.sender().setStyleSheet('')
        curveStats = ['Jump SLOPE [pN/nm]','ADHESION [pN]','Stretch AREA [fJ]','DETACH-X [nm]','DETACH-F [pN]','AREA [fJ]','NTRAITS','NJUMPS','NPLATEAUX','Max Step [pN]']

        currentStat = self.ui.whichStat.currentText()

        self.ui.stat.clear()
        self.clearLegend()

        self.ui.stat.plotItem.legend.items = []
        while self.ui.stat.plotItem.legend.layout.count() > 0:
            self.ui.stat.plotItem.legend.layout.removeAt(0)

        if self.exp.segmented is False:
            self.segmentAll()

        isFiltered = self.ui.filters_group.isChecked()
        isNoEmpty = self.ui.filter_empty.isChecked()

        data = []
        families = []

        for cv in self.exp:
            if isNoEmpty is True:
                fTh = self.ui.minJump.value()
                if cv.hasFished(fTh,self.ui.arBlue.isChecked()) is False:
                    continue
            if isFiltered is True:
                dnum = len(cv['up'].traits)
                if dnum < self.ui.lim_min_ntraits.value() or dnum > self.ui.lim_max_ntraits.value():
                    continue
                dpoint = cv['up'].getDetachPoint()
                if dpoint > self.ui.lim_max_detach.value() or dpoint < self.ui.lim_min_detach.value():
                    continue
            else:
                dpoint = cv['up'].getDetachPoint()
            if currentStat in curveStats:
                if currentStat == 'ADHESION [pN]':
                    number = cv['up'].getAdhesion()
                elif currentStat == 'Stretch AREA [fJ]':
                    number = cv.getStretchArea(self.ui.arBlue.isChecked())
                elif currentStat == 'DETACH-X [nm]':
                    number = dpoint
                elif currentStat=='Jump SLOPE [pN/nm]':
                    number = cv.getJumpSlope()
                elif currentStat == 'DETACH-F [pN]':
                    number = cv.getDetachForce()
                elif currentStat=='Max Step [pN]':
                    number = cv['up'].getMaxStep(isFiltered,[self.ui.lim_min_xtrait.value() ,self.ui.lim_max_xtrait.value() ],[self.ui.lim_min_length.value(),self.ui.lim_max_length.value()])
                elif currentStat=='AREA [fJ]':
                    number = cv['up'].getArea( reflatten=self.ui.reflatten.isChecked(),polyorder=self.ui.derorder.value())
                elif currentStat in ['NTRAITS','NJUMPS','NPLATEAUX']:
                    nump,numj,numb = cv['up'].getNumbers()
                    if currentStat=='NTRAITS':
                        number = nump+numj+numb
                    elif currentStat == 'NJUMPS':
                        number = numj
                    elif currentStat == 'NPLATEAUX':
                        number = nump
                if number is not None:
                    data.append(number)
                    families.append(cv.family)
            else:
                isJump = self.ui.lim_isJump.isChecked()
                isPlat = self.ui.lim_isPlat.isChecked()
                if len(cv['up'].traits)<2:
                    next
                first = True
                for t in cv['up'].traits:
                    if first is False:
                        if t.accept is True:
                            if isFiltered is True:
                                if (isPlat is False and t.pj=='P') or (isJump is False and t.pj=='J'):
                                    continue
                                dmin = min(t.x)
                                if dmin < self.ui.lim_min_xtrait.value() or dmin > self.ui.lim_max_xtrait.value():
                                    continue
                                dlen = t.alen()
                                if dlen < self.ui.lim_min_length.value() or dlen > self.ui.lim_max_length.value():
                                    continue
                            if 'LENGTH' in currentStat:
                                number = t.alen()
                            elif 'POSITION' in currentStat:
                                number = min(t.x)
                            elif 'STEP' in currentStat:
                                number = t.height
                            elif 'SLOPE' in currentStat:
                                number = t.slope(angle=False)
                            data.append(number)
                            families.append(cv.family)
                    first = False

        gx = []
        gy = []

        if len(data)==0:
            return

        data = np.array(data)
        families = np.array(families)
        ibad = grubbs.two_sided_test_indices(data,alpha=0.05)
        mask = np.ones(data.shape,dtype=bool)
        mask[ibad]=False

        data = data[mask]
        families = families[mask]

        if self.ui.lim_custom.isChecked() is False:
            self.ui.lim_min_range.setMinimum(min(data))
            self.ui.lim_min_range.setMaximum(max(data))
            self.ui.lim_max_range.setMinimum(min(data))
            self.ui.lim_max_range.setMaximum(max(data))
            bn = 'auto'
            rng = (min(data),max(data))
        else:
            bn = self.ui.lim_bins.value()
            if bn == 0:
                bn = 'auto'
            rng = (self.ui.lim_min_range.value(),self.ui.lim_max_range.value())

        if self.ui.separateFamilies.isChecked() is True:
            for j in range( int(self.ui.cFamilyLoad.maximum() ) ):
                dx = data[families==j+1]
                if currentStat in ['NTRAITS','NJUMPS','NPLATEAUX']:
                    y,xi = np.histogram(dx, bins=min(max(dx),max(rng)), normed=True, range=rng)
                else:
                    y,xi = np.histogram(dx, bins=bn, normed=True, range=rng)
                xx = xi[1:]+xi[:-1]/2
                gx.append(xx)
                gy.append(y)
        else:
            if currentStat in ['NTRAITS','NJUMPS','NPLATEAUX']:
                y,xi = np.histogram(data, bins=min(max(data),max(rng)), normed=True, range=rng)
            else:
                y,xi = np.histogram(data, bins=bn, normed=True, range=rng)
            xx = xi[1:]+xi[:-1]/2
            gx.append(xx)
            gy.append(y)

        colors = [QtGui.QColor(0,0,255),QtGui.QColor(0,255,0),QtGui.QColor(255,0,0),QtGui.QColor(0,255,255),QtGui.QColor(255,255,0),QtGui.QColor(255,0,255)]
        for i in range(len(gx)):
            col = colors[i%len(colors)]
            colTra = col
            colTra.setAlpha(127)
            xtofit = gx[i]
            ytofit = gy[i]


            self.ui.stat.plot(xtofit,ytofit,pen=None,symbolBrush=colTra,symbolSize=5,name='FAM{}'.format(i+1))

            if self.ui.fit_gauss.isChecked() is True:
                try:
                    def gauss(x,y0,A,x0,sigma):
                        return y0+A*np.exp(-(x-x0)**2/sigma**2)
                    popt =  curve_fit(gauss, xtofit, ytofit, p0=[0.0,max(ytofit),xtofit[np.argmax(ytofit)],(max(xtofit)-min(xtofit))/10.0])
                    xx = np.linspace(min(xtofit),max(xtofit),1000)
                    self.ui.stat.plot(xx,gauss(xx,*popt[0]),pen= col, name='FAM{} fit x0={:.4g}'.format(i+1,popt[0][2]))
                except:
                    print('Gauss fit not suitable')

            if self.ui.fit_decay.isChecked() is True:
                try:
                    def decay(x,y0,A,deltax):
                        return y0+A*np.exp(-(x/deltax))
                    popt =  curve_fit(decay, xtofit, ytofit, p0=[0.0,ytofit[0],(max(xtofit)-min(xtofit))/10.0])
                    xx = np.linspace(min(xtofit),max(xtofit),1000)
                    self.ui.stat.plot(xx,decay(xx,*popt[0]),pen=col,name='FAM{} fit dx={:.4g}'.format(i+1,popt[0][2]))
                except:
                    print('Decay fit not suitable')

    def addFamily(self):
        newMax = self.ui.cFamilyLoad.maximum()+1
        self.ui.cFamilyLoad.setMaximum(newMax )
        self.ui.cFamily.setMaximum(newMax)
        self.ui.cNumFam.setText(str(newMax))
        self.ui.cFamilyLoad.setValue(newMax)

    def setConnections(self):

        clickable1=[self.ui.reflatten,self.ui.radio_traits,self.ui.radio_view,self.ui.radio_deriv,self.ui.radio_smooth,self.ui.radio_area,self.ui.arBlue,self.ui.arGreen]
        editable =[self.ui.derorder,self.ui.s_mth,self.ui.s_vth,self.ui.sg_fw,self.ui.sg_mm,self.ui.plath,self.ui.lasth,self.ui.str_lim]
        for o in clickable1:
            o.clicked.connect(self.refreshCurve)
        for o in editable:
            o.editingFinished.connect(self.updateCurve)
            o.valueChanged.connect(self.reddish)

        self.ui.cscope.clicked.connect(self.chCustom)
        self.ui.bAddFile.clicked.connect(self.addFile)
        self.ui.bAddFiles.clicked.connect(self.addFiles)
        self.ui.bAddDir.clicked.connect(self.addDir)
        self.ui.bAddFamily.clicked.connect(self.addFamily)
        self.ui.btn_flatten.clicked.connect(self.flatten)
        self.ui.btn_recalibrate.clicked.connect(self.rescale)
        self.ui.btn_popout.clicked.connect(self.popout)

        self.ui.bReset.clicked.connect(self.resetAll)
        self.ui.bDoSave.clicked.connect(self.statSave)

        self.ui.plotStat.clicked.connect(self.dostat)
        self.ui.whichStat.currentIndexChanged.connect(self.chStat)
        self.ui.redoStat.clicked.connect(self.redoStat)

        self.ui.pjbar.valueChanged.connect(self.refreshPJ)
        self.ui.cbar.valueChanged.connect(self.changeCurve)

        QtCore.QMetaObject.connectSlotsByName(self)

    def viewCurve(self,autorange=True):
        #XXX
        #QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        ism = self.ui.radio_smooth.isChecked()
        isa = self.ui.radio_area.isChecked()
        isd = self.ui.radio_deriv.isChecked()
        ist = self.ui.radio_traits.isChecked()

        self.ui.grafo.clear()
        if len(self.curve)>0:
            p = self.curve['up']

            #ifrom = np.argmax(p.f)
            x = p.z#[ifrom:]
            y = p.f#[ifrom:]
            ar = None

            self.statusBar().showMessage(self.curve.filename)

            if isd is True:
                der = getSG(p.f, p.segmentation.abswin(p), p.segmentation.filtorder, deriv=1)
                self.ui.grafo.plot(x,der,pen='b')
                if autorange:
                    self.ui.grafo.autoRange()
                xx = np.linspace(x[0],x[-1],3)
                yy = np.ones(3)*self.curve['up'].segmentation.absth(p)
                self.ui.grafo.plot(xx,yy,pen='r')
                self.ui.grafo.plot(xx,-yy,pen='r')

                #iborders = p.segmentation.run(p,debug=True)
                #self.ui.grafo.plot(x[iborders],der[iborders],pen=pg.mkPen(None),symbolBrush=(255,0,0), symbolPen='k')


            else:
                if isa is True:
                    self.ui.grafo.plot(x,y,pen='k',fillLevel=0,brush =  pg.mkBrush(0,0,255,100))
                else:
                    self.ui.grafo.plot(x,y,pen='k')

                if ism is True:
                    y2 = getSG(y,filtwidth=self.curve['up'].segmentation.abswin(p),deriv=0)
                    self.ui.grafo.plot(x,y2,pen='b')
                    if autorange:
                        self.ui.grafo.autoRange()
                #y2 = sg.getSG(y,filtwidth=self.curve[-1].segmentation.abswin,deriv=0)
                else:
                    #contact and detach points
                    zcontact,fcontact = self.curve['up'].getOrigin()
                    zdetach,fdetach = self.curve['up'].getJumpPoint()
                    znearfar,fnearfar = self.curve['up'].getNearFarPoint()
                    self.ui.grafo.plot([zcontact],[fcontact],symbolPen='r', symbolSize=12, symbolBrush=(255, 0, 0, 50))
                    self.ui.grafo.plot([zdetach],[fdetach],symbolPen='g', symbolSize=12, symbolBrush=(0, 255, 0, 50))
                    self.ui.grafo.plot([znearfar],[fnearfar],symbolPen='b', symbolSize=12, symbolBrush=(0, 0, 255, 50))

                    #self.ui.grafo.plot(x,y2,pen='b')
                    if len(self.curve['up'].traits)==0:
                        return
                    i=2
                    j=2
                    for ss in self.curve['up'].traits:
                        if ss.accept:
                            if ss.first is True:
                                if ss.pj=='J':
                                    j+=1
                                else:
                                    i+=1
                            if ss.pj=='J':
                                if j%2 == 0:
                                    c = self.color_jump1
                                else:
                                    c = self.color_jump2
                            else:
                                if i%2 == 0:
                                    c = self.color_plateaux1
                                else:
                                    c = self.color_plateaux2
                        else:
                            c = self.color_bad
                        tro = self.ui.derorder.value()
                        if ist is True:
                            sx,sy = ss.getPoints(mode='curve')
                        else:
                            if tro==1:
                                sx,sy = ss.getPoints(mode='lin')
                            else:
                                sx,sy = ss.getPoints(mode='poly',polyorder=tro)
                        self.ui.grafo.plot(sx,sy,pen=c)
                        self.ui.riga = pg.LinearRegionItem(movable=False)
                        self.ui.grafo.addItem(self.ui.riga)
                    if isa is True and self.ui.reflatten.isChecked() is True:
                        sx,sy = self.curve['up'].traits[0].getPoints(mode='poly',polyorder=tro,extend=True)
                        self.ui.grafo.plot(sx,sy,pen=pg.mkPen(color='k',style=QtCore.Qt.DashLine))
                    if autorange:
                        self.ui.grafo.autoRange()
                        #if (isc is True) and (ar != None):
                            #self.ui.grafo.setRange(xRange=(0,ar))
                        if (isa is True) and (ar != None):
                            self.ui.grafo.plot(x,y,pen='k')


        #QtWidgets.QApplication.restoreOverrideCursor()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName( 'qt-ONE-View' )
    canale = CurveWindow()
    canale.show()
    #QtCore.QObject.connect( app, QtCore.SIGNAL( 'lastWindowClosed()' ), app, QtCore.SLOT( 'quit()' ) )
    sys.exit(app.exec_())
