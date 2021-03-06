#!/usr/in/env python
# -*- coding: utf-8 -*-
#
#       qgsRasterStats.py
#       
#       Copyright 2010 GeoINTA Team geointa@cnia.inta.gov.ar
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from qgsStatsForm import Ui_qgsStatsForm
from poly2geojson import *
from qgsRasterProcess import RasterProcess
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis import *
from qgis.core import *
from qgis.gui import * 
import sys, os



class qgsRasterStatsUI(QDialog, Ui_qgsStatsForm):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_qgsStatsForm()
        self.ui.setupUi(self)
        

class RasterStats: 
    """RasterStats es el plugin
    """
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        
    def initGui(self):  
        self.form_plugin = qgsRasterStatsUI()
        self.action = QAction(QIcon(":/img/logo.png"), "Raster Stats by Features", self.iface.mainWindow())
        QObject.connect(self.action, SIGNAL("triggered()"), self.run) 
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Raster Stats by Features", self.action)
        
        QObject.connect(self.form_plugin.ui.btnOutFileResult, SIGNAL("clicked()"), self.save_output_results)
        QObject.connect(self.form_plugin.ui.btnRasterDir, SIGNAL("clicked()"), self.select_dir_rasters)
        QObject.connect(self.form_plugin.ui.btnGDALPath, SIGNAL("clicked()"), self.select_path_gdal)
        QObject.connect(self.form_plugin.ui.btnStart, SIGNAL("clicked()"), self.start)
        
    def unload(self):
        self.iface.removePluginMenu("&Raster Stats by Features", self.action)
        self.iface.removeToolBarIcon(self.action)
    
    def run(self):
        if not self.canvas.currentLayer() and not type(self.canvas.currentLayer()) == QgsVectorLayer:
            QMessageBox.information(self.form_plugin, u'Error', u'There isn\'t one vector layer selected')
            return
    
        self.layerCurrent = self.canvas.currentLayer() # It's the vector layer for cut
    
        self.form_plugin.setWindowFlags( Qt.WindowStaysOnTopHint )
        self.form_plugin.show()
        self.form_plugin.ui.txtCurrentVectorLayer.setText(self.canvas.currentLayer().name())
        self.form_plugin.ui.txtGDALPath.setText("/usr/bin/gdalwarp")
        
        self.provider = self.layerCurrent.dataProvider()
        
        for qfield in self.provider.fields():
            self.form_plugin.ui.cboFields.addItem(qfield.name())
            

    def save_output_results(self):
        file = QFileDialog.getSaveFileName(self.form_plugin, "Save outpus results as...", os.path.expanduser('~'), "CSV (*.csv)")
        if not file:
            return
        if not str(file).endswith('.csv'):
            file += '.csv'
        self.form_plugin.ui.txtOutputFileResult.setText(file)
        
    def select_dir_rasters(self):
        file = QFileDialog.getExistingDirectory(self.form_plugin, "Select directory...", os.path.expanduser('~'), QFileDialog.ShowDirsOnly)
        if not file:
            return
        if not str(file).endswith('/'):
            file += '/'
        self.form_plugin.ui.txtPathDirRasters.setText(file)
    
    def select_path_gdal(self):
        file = QFileDialog.getOpenFileName(self.form_plugin, "Open gdalwrap command...", os.path.expanduser('~'), "gdalwrap (gdalwrap*)")
        if not file:
            return
        self.form_plugin.ui.txtGDALPath.setText(file)
    

    def start(self):
        self.form_plugin.ui.lstLogs.clear()
        self.form_plugin.ui.lstLogs.addItem("Vector Layer: " + self.form_plugin.ui.txtCurrentVectorLayer.text())
        self.form_plugin.ui.lstLogs.addItem("Rasters directory: " + self.form_plugin.ui.txtPathDirRasters.text())
        self.form_plugin.ui.lstLogs.addItem("Rasters NoData: " + self.form_plugin.ui.txtNoData.text())
        self.form_plugin.ui.lstLogs.addItem("GDALPath: " + self.form_plugin.ui.txtGDALPath.text())
        
        self.po2json = poly2GeoJSON()
        
        rp = RasterProcess(cmd = self.form_plugin.ui.txtGDALPath.text(), NoData = int(self.form_plugin.ui.txtNoData.text()), dir_raster = self.form_plugin.ui.txtPathDirRasters.text(), out = self.form_plugin.ui.txtOutputFileResult.text())
        
        # ----  Before API version  ----
        #~ feat = QgsFeature()
        #~ allAttrs = self.provider.attributeIndexes()
        #~ print dir(self.provider)
        #~ self.provider.select(allAttrs)
        
        # For each feature in the vector layer!
        #~ while self.provider.nextFeature(feat):
        for feat in self.layerCurrent.getFeatures():
            f = GeoJSONFeature(id = feat.id(), type = "Polygon")
            
            # WARNING: I don't know how it answer to ring vectors. I don't check it
            geom = [list(x) for x in feat.geometry().asPolygon()[0]]
            
            f.set_coordinates(geom)
            self.po2json.set_feature(f.dump())
            #attrs = feat.attributeMap()[self.form_plugin.ui.cboFields.currentIndex()]
            aux_id = feat[self.form_plugin.ui.cboFields.currentIndex()]
            self.form_plugin.ui.lstLogs.addItem("Fid: %i %s %i"%(f.feature['id'], self.form_plugin.ui.cboFields.currentText(), aux_id))
            rp.set_feature(aux_id, self.po2json.dump())
            rp.start()
        self.form_plugin.ui.lstLogs.addItem("Listo!")

    
        
def main():
    
    return 0

if __name__ == '__main__':
	main()
