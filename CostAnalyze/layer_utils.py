from PyQt4.QtCore import *
from qgis.core import *
from qgis.utils import *
import gdal

def pixelOffsets2coords(rasterLayer, pixelOffsets):
    provider = rasterLayer.dataProvider()
    raster = gdal.Open(str(provider.dataSourceUri()), gdal.GA_Update)
    geoTransform = raster.GetGeoTransform()
    coords = []
    for pixelOffset in pixelOffsets:
        originX = geoTransform[0]
        originY = geoTransform[3]
        pixelWidth = geoTransform[1]
        pixelHeight = geoTransform[5]
        coordX = originX + pixelWidth * pixelOffset[0]
        coordY = originY + pixelHeight * pixelOffset[1]
        coords.append([coordX, coordY])
    return coords

def coords2pixelOffsets(rasterLayer, coords):
    provider = rasterLayer.dataProvider()
    raster = gdal.Open(str(provider.dataSourceUri()), gdal.GA_Update)
    geoTransform = raster.GetGeoTransform()
    pixelOffsets = []
    for coord in coords:
        originX = geoTransform[0]
        originY = geoTransform[3]
        pixelWidth = geoTransform[1]
        pixelHeight = geoTransform[5]
        pixelOffsetX = (coord[0] - originX) / pixelWidth
        pixelOffsetY = (coord[1] - originY) / pixelHeight
        pixelOffsets.append([pixelOffsetX, pixelOffsetY])
    return pixelOffsets

def create_path_layer(map, cost_layer):
    path = map["path"]
    method = map["method"]
    cost = map["cost"]
    time = map["time"]

    path_length = len(path)
    path_layer_name = "cost_analyze_" + cost_layer.name() + "_" + method + "_" + str(path[0][0]) + "-" + str(
        path[0][1]) + "_" \
                      + str(path[path_length - 1][0]) + "-" + str(path[path_length - 1][1])
    path_layer = QgsVectorLayer("LineString", path_layer_name, "memory")

    data_provider = path_layer.dataProvider()

    path_layer.startEditing()
    data_provider.addAttributes([
        QgsField("layer_name", QVariant.String),
        QgsField("start_point_x", QVariant.String),
        QgsField("start_point_y", QVariant.String),
        QgsField("end_point_x", QVariant.String),
        QgsField("end_point_y", QVariant.String),
        QgsField("method", QVariant.String),
        QgsField("cost", QVariant.String),
        QgsField("time", QVariant.String)])

    path_feature = QgsFeature()
    path_coords = pixelOffsets2coords(cost_layer, path)
    path_point_list = []
    for point in path_coords:
        q_point = QgsPoint(point[0], point[1])
        path_point_list.append(q_point)
    path_feature.setGeometry(QgsGeometry.fromPolyline(path_point_list))

    # path_feature["layer_name"] = cost_layer.name
    path_feature.setAttributes([str(cost_layer.name()), str(path[0][0]), str(path[0][1]),
                                str(path[len(path) - 1][0]), str(path[len(path) - 1][1]),
                                str(method), str(cost), str(time)])
    data_provider.addFeatures([path_feature])
    path_layer.commitChanges()
    symbols = path_layer.rendererV2().symbols()
    symbol = symbols[0]
    symbol.setWidth(1)
    path_layer.triggerRepaint()
    return path_layer

def get_cost_array(raster_layer):
    data_provider = raster_layer.dataProvider()
    raster = gdal.Open(str(data_provider.dataSourceUri()), gdal.GA_Update)
    band = raster.GetRasterBand(1)
    cost = band.ReadAsArray()
    return cost
