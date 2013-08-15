def name():
  return "Raster Stats by Features"

def description():
  return "This plugin calculate stats data about to some rasters for each feature"

def version():
  return "Version 0.1"

def qgisMinimumVersion():
  return "1.0"

def authorName():
  return "GeoINTA Team"

def classFactory(iface):
  # load TestPlugin class from file testplugin.py
  from qgsRasterStats import RasterStats
  return RasterStats(iface)
