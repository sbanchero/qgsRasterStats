#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  poly2GeoJSON.py
#  
#  Copyright 2013 Santiago Banchero <santiago@geopistol>
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

import json

class poly2GeoJSON:
    def __init__(self):
        self.json = {"type": "FeatureCollection", "features": []}
    
    def add_feature(self, feat):
        self.json["features"].append(feat)
    
    def set_feature(self, feat):
        self.json["features"] = [feat]
    
    def dump(self):
        return json.dumps(self.json)

class GeoJSONFeature:
    def __init__(self, id = None, type = None):
        self.feature = {"type": "Feature", "properties": {}, "id": id, "geometry": {"type": type, "coordinates": None}}
        
    def set_id(self, id):
        self.feature["id"] = id

    def set_type(self, type):
        self.feature["geometry"]["type"] = type
    
    def set_coordinates(self, coord):
        self.feature["geometry"]["coordinates"] = [coord]
    
    def dump(self):
        return self.feature


def main():
	
	return 0

if __name__ == '__main__':
	main()

