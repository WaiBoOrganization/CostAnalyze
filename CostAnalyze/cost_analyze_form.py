# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cost_analyze_form.ui'
#
# Created: Fri Dec 21 10:31:57 2018
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(661, 421)
        self.costSelector = QtGui.QComboBox(Dialog)
        self.costSelector.setGeometry(QtCore.QRect(120, 10, 261, 22))
        self.costSelector.setObjectName(_fromUtf8("costSelector"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 151, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 151, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 151, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.AlgorithmSelector = QtGui.QComboBox(Dialog)
        self.AlgorithmSelector.setGeometry(QtCore.QRect(120, 100, 261, 22))
        self.AlgorithmSelector.setObjectName(_fromUtf8("AlgorithmSelector"))
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(290, 130, 91, 31))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.startPointX = QtGui.QLineEdit(Dialog)
        self.startPointX.setGeometry(QtCore.QRect(120, 40, 111, 21))
        self.startPointX.setObjectName(_fromUtf8("startPointX"))
        self.endPointY = QtGui.QLineEdit(Dialog)
        self.endPointY.setGeometry(QtCore.QRect(240, 70, 111, 21))
        self.endPointY.setObjectName(_fromUtf8("endPointY"))
        self.startPointY = QtGui.QLineEdit(Dialog)
        self.startPointY.setGeometry(QtCore.QRect(240, 40, 111, 21))
        self.startPointY.setObjectName(_fromUtf8("startPointY"))
        self.endPointX = QtGui.QLineEdit(Dialog)
        self.endPointX.setGeometry(QtCore.QRect(120, 70, 111, 21))
        self.endPointX.setObjectName(_fromUtf8("endPointX"))
        self.tableView = QtGui.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(10, 170, 371, 211))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.getStartPointBtn = QtGui.QPushButton(Dialog)
        self.getStartPointBtn.setGeometry(QtCore.QRect(360, 40, 21, 21))
        self.getStartPointBtn.setObjectName(_fromUtf8("getStartPointBtn"))
        self.getEndPointBtn = QtGui.QPushButton(Dialog)
        self.getEndPointBtn.setGeometry(QtCore.QRect(360, 70, 21, 21))
        self.getEndPointBtn.setObjectName(_fromUtf8("getEndPointBtn"))
        self.textBrowser = QtGui.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(390, 10, 261, 371))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(90, 390, 561, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 390, 101, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Cost Analyze", None))
        self.label.setText(_translate("Dialog", "Cost Layer：", None))
        self.label_2.setText(_translate("Dialog", "Start Point:", None))
        self.label_3.setText(_translate("Dialog", "End Point:", None))
        self.label_4.setText(_translate("Dialog", "Algorithm:", None))
        self.okButton.setText(_translate("Dialog", "execute", None))
        self.getStartPointBtn.setText(_translate("Dialog", "+", None))
        self.getEndPointBtn.setText(_translate("Dialog", "+", None))
        self.label_5.setText(_translate("Dialog", "Progress：", None))

