# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4 import QtCore
from qgis.utils import *
from qgis.gui import QgsMapTool

from cost_analyze_form import *
#from algorithms.astar import *
#from algorithms.SPFA import *
from algorithms.dijkstra import *
from algorithms.algorithms import *

from layer_utils import *
import thread
import math
import time
import resources

class CostAnalyze:
    def __init__(self, iface):
        self.iface = iface
        self.rasterLayers = []
        self.inputMode = 0

    def initGui(self):
        self.action = QAction(QIcon(":/plugins/CostAnalyze/icon.png"), "Cost Analyze", self.iface.mainWindow())
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Raster Analyze", self.action)

    def unload(self):
        self.iface.removePluginMenu("&Raster Analyze", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        self.window = QWidget()
        self.window.setWindowTitle("Cost Analyze")
        self.window.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.main = Ui_Dialog()
        self.main.setupUi(self.window)
        self.load_layer_names()
        # connect to function
        self.main.okButton.clicked.connect(self.calculate)
        self.main.getStartPointBtn.clicked.connect(self.inputStart)
        self.main.getEndPointBtn.clicked.connect(self.inputEnd)
        click_tool = ClickTool(parent=self)
        self.iface.mapCanvas().setMapTool(click_tool)
        self.executeTime = -1
        self.model = QStandardItemModel(100, 3)
        self.model.setHorizontalHeaderLabels(["Algorithm", "Cost", "Time"])
        self.main.tableView.setModel(self.model)
        self.main.textBrowser.setOpenExternalLinks(True)
        self.main.textBrowser.setText("1 Add a raster layer to the Qgis. Then select the raster layer as the cost layer.\n"
                                      "2 Click on the '+' then click on the raster layer map to add a 'Start Point' and a 'End Point'.\n"
                                      "3 Select an algorithm and click on the 'execute' button.\n"
                                      "4 The minimum cost and time cost will be shown below.\n\n"
                                      )
        self.main.textBrowser.append("Github: <a href=https://github.com/WaiBoOrganization/CostAnalyze>"
                                     "https://github.com/WaiBoOrganization/CostAnalyze</a>")
        self.window.show()

    def load_layer_names(self):
        # load layer name
        mapCanvas = iface.mapCanvas()
        layers = mapCanvas.layers()
        raster_layer_names = []
        for layer in layers:
            if layer.type() == QgsMapLayer.RasterLayer:
                self.rasterLayers.append(layer)
                raster_layer_names.append(layer.name())
        self.main.costSelector.addItems(raster_layer_names)
        # load algorithm name
        algorithm_names = ["SPFA", "SLF","LLL", "SLF&LLL", "Dijkstra", "A*", "All"]
        self.main.AlgorithmSelector.addItems(algorithm_names)

    def QString2PyString(self, qStr):
        return unicode(qStr.toUtf8(), 'utf-8', 'ignore')

    def inputStart(self):
        self.inputMode = 1

    def inputEnd(self):
        self.inputMode = 2

    def calculate(self):
        # read start and end point
        startX = int(self.main.startPointX.text())
        startY = int(self.main.startPointY.text())
        endX = int(self.main.endPointX.text())
        endY = int(self.main.endPointY.text())
        # read image data
        costLayer = self.rasterLayers[self.main.costSelector.currentIndex()]
        cost_array = get_cost_array(costLayer)
        # progress bar
        progressBar = self.main.progressBar
        #self.worker = Worker()
        #self.worker.progress.connect(self.main.progressBar.setValue)
        #self.worker.start()
        # using algorithm
        if self.main.AlgorithmSelector.currentIndex() == 0:
            map = SPFA(cost_array, startX, startY, endX, endY, progressBar)
            self.showItems(map, costLayer)
            progressBar.setValue(0)
        elif self.main.AlgorithmSelector.currentIndex() == 1:
            map = SLF(cost_array, startX, startY, endX, endY, progressBar)
            self.showItems(map, costLayer)
            progressBar.setValue(0)
        elif self.main.AlgorithmSelector.currentIndex() == 2:
            map = LLL(cost_array, startX, startY, endX, endY, progressBar)
            self.showItems(map, costLayer)
            progressBar.setValue(0)
        elif self.main.AlgorithmSelector.currentIndex() == 3:
            map = SLFandLLL(cost_array, startX, startY, endX, endY, progressBar)
            self.showItems(map, costLayer)
            progressBar.setValue(0)
        elif self.main.AlgorithmSelector.currentIndex() == 4:
            map = dijkstra(cost_array, startX, startY, endX, endY)
            self.showItems(map, costLayer)
            progressBar.setValue(0)
        elif self.main.AlgorithmSelector.currentIndex() == 5:
            map = astar(cost_array, startX, startY, endX, endY, progressBar)
            self.showItems(map, costLayer)
            progressBar.setValue(0)
        elif self.main.AlgorithmSelector.currentIndex() == 6:
            map = SPFA(cost_array, startX, startY, endX, endY, progressBar)
            self.showItems(map, costLayer)
            progressBar.setValue(0)
            map = SLF(cost_array, startX, startY, endX, endY, progressBar)
            self.showItems(map, costLayer)
            progressBar.setValue(0)
            map = LLL(cost_array, startX, startY, endX, endY, progressBar)
            self.showItems(map, costLayer)
            progressBar.setValue(0)
            map = SLFandLLL(cost_array, startX, startY, endX, endY, progressBar)
            self.showItems(map, costLayer)
            progressBar.setValue(0)
            map = dijkstra(cost_array, startX, startY, endX, endY)
            self.showItems(map, costLayer)
            progressBar.setValue(0)
            map = astar(cost_array, startX, startY, endX, endY, progressBar)
            self.showItems(map, costLayer)
            progressBar.setValue(0)

    def showItems(self, map, costLayer):
        self.executeTime += 1
        self.model.setItem(self.executeTime, 0, QStandardItem(str(map["method"])))
        self.model.setItem(self.executeTime, 1, QStandardItem(str(map["cost"])))
        self.model.setItem(self.executeTime, 2, QStandardItem(str(map["time"])))
        # create path layer
        path_layer = create_path_layer(map, costLayer)
        # add layer to the registry
        QgsMapLayerRegistry.instance().addMapLayer(path_layer)

#Inherit from QThread
class Worker(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal(bool)
    def run(self):
        global PROGRESS
        while PROGRESS <= 1:
            self.progress.emit(int(PROGRESS*100))
            if PROGRESS == 1:
                break
            time.sleep(0.1)
        self.finished.emit(True)



# 点击确定起止点
class ClickTool(QgsMapTool):
    def __init__(self, parent):
        QgsMapTool.__init__(self, parent.iface.mapCanvas())
        self.parent = parent
        self.canvas = parent.iface.mapCanvas()
        self.main = parent.main

    def canvasPressEvent(self, QgsMapMouseEvent):
        if QgsMapMouseEvent.button() == Qt.LeftButton:
            x = QgsMapMouseEvent.pos().x()
            y = QgsMapMouseEvent.pos().y()
            # 每次点击都先判断当前的activeLayer
            layer_name = self.main.costSelector.currentText()
            for layer in self.canvas.layers():
                if layer.name() == layer_name:
                    self.activeLayer = layer
                    break
            self.data_provider = self.activeLayer.dataProvider()
            self.extent = self.data_provider.extent()
            self.width = self.data_provider.xSize() if self.data_provider.capabilities() & self.data_provider.Size else 1000
            self.height = self.data_provider.ySize() if self.data_provider.capabilities() & self.data_provider.Size else 1000
            self.xres = self.extent.width() / self.width
            self.yres = self.extent.height() / self.height
            point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            if self.extent.xMinimum() <= point.x() <= self.extent.xMaximum() and self.extent.yMinimum() <= point.y() <= self.extent.yMaximum():
                col = int(math.floor((point.x() - self.extent.xMinimum()) / self.xres))
                row = int(math.floor((self.extent.yMaximum() - point.y()) / self.yres))
                current_x = col * self.xres + self.extent.xMinimum()
                current_y = self.extent.yMaximum() - row * self.yres
                if self.parent.inputMode == 1:
                    self.main.startPointX.setText(str(col))
                    self.main.startPointY.setText(str(row))
                    self.addPoint(current_x, current_y, 1)
                elif self.parent.inputMode == 2:
                    self.main.endPointX.setText(str(col))
                    self.main.endPointY.setText(str(row))
                    self.addPoint(current_x, current_y, 2)
                self.parent.inputMode = 0

    def addPoint(self, x, y, mode):
        if mode == 1:
            for layer in self.canvas.layers():
                if layer.name() == "Start":
                    QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            vector = QgsVectorLayer("Point", "Start", "memory")
            vector.startEditing()
            vpr = vector.dataProvider()
            pnt = QgsGeometry.fromPoint(QgsPoint(x, y))
            f = QgsFeature()
            f.setGeometry(pnt)
            vpr.addFeatures([f])
            vector.updateExtents()
            vector.commitChanges()
            symbols = vector.rendererV2().symbols()
            symbol = symbols[0]
            symbol.setColor(QColor("green"))
            symbol.setSize(3)
            vector.triggerRepaint()
            QgsMapLayerRegistry.instance().addMapLayer(vector)
        else:
            for layer in self.canvas.layers():
                if layer.name() == "End":
                    QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            vector = QgsVectorLayer("Point", "End", "memory")
            vector.startEditing()
            vpr = vector.dataProvider()
            pnt = QgsGeometry.fromPoint(QgsPoint(x, y))
            f = QgsFeature()
            f.setGeometry(pnt)
            vpr.addFeatures([f])
            vector.updateExtents()
            vector.commitChanges()
            symbols = vector.rendererV2().symbols()
            symbol = symbols[0]
            symbol.setColor(QColor("red"))
            symbol.setSize(3)
            vector.triggerRepaint()
            QgsMapLayerRegistry.instance().addMapLayer(vector)

