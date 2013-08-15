#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  qgsRasterProcess.py
#  
#  Copyright 2013 Santiago Banchero <santiago@geofreedom>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from subprocess import Popen, PIPE
from os import listdir, path
from osgeo import gdal

class RasterProcess:
    def __init__(self, cmd = None, NoData = None, dir_raster = None, out = None):
        self.cmd = str(cmd)
        self.NoData = NoData
        self.out = str(out)
        self.dir_raster = str(dir_raster)
        self.file_json = None
        self.calc = CalculateStats()
        self.current_id_clip = None
        

    def set_feature(self, name, feat_json):
        try:
            self.file_json = self.dir_raster + 'poly_' + str(name) + '.json'
            self.current_id_clip = name
            open(self.file_json, 'w').write(feat_json)
        except Exception, e:
            print e, "ERROR: Can't save geojson: %s"%(self.file_json), feat_json

    def start(self):
        self.command = [self.cmd, '-overwrite','-q','-dstnodata', str(self.NoData), '-cutline', self.file_json, '-of', 'GTiff']
        for img in listdir(self.dir_raster):
            if img.endswith('tif'):
                # clipper image with the vector
                cdo = self.command + [self.dir_raster + img, self.out + '.tif']
                p = Popen(cdo, stdout=PIPE)
                p.wait()
                self.calc.clipper_process(name = img, img_file_path = self.out + '.tif', id_clip = self.current_id_clip, NoData= self.NoData)
        
        fout = open(self.out, 'w')
        fout.write('raster,id_poly,band,min,max,mean,var\n')
        for img in self.calc.results:
            fout.write("%s,%s,%s,%s,%s,%s,%s\n" % (tuple(img)))
        fout.close()
        
class CalculateStats:
    def __init__(self):
        self.results = []
    
    def clipper_process(self, name = None, img_file_path = None, id_clip = None, NoData = None):
        self.ds = gdal.Open(img_file_path, gdal.GA_ReadOnly)
        for b in range(self.ds.RasterCount):
            band = self.ds.GetRasterBand(b + 1)
            data = band.ReadAsArray()[band.ReadAsArray() <> NoData] #Filter NoData Values to do stats

            self.results.append([name, id_clip, b + 1,  data.min(), data.max(), data.mean(),data.var()])
            
            print self.results
        

def main():
	
	return 0

if __name__ == '__main__':
	main()

