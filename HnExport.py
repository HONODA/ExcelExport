# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HnExport.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 400)
        Dialog.setMinimumSize(QtCore.QSize(600, 400))
        Dialog.setMaximumSize(QtCore.QSize(600, 400))
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(400, 0, 160, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.export_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.export_button.setObjectName("export_button")
        self.verticalLayout.addWidget(self.export_button)
        self.select_all_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.select_all_button.setObjectName("select_all_button")
        self.verticalLayout.addWidget(self.select_all_button)
        self.clear_all_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.clear_all_button.setObjectName("clear_all_button")
        self.verticalLayout.addWidget(self.clear_all_button)
        self.close_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.close_button.setObjectName("close_button")
        self.verticalLayout.addWidget(self.close_button)
        self.Suplierlist = QtWidgets.QListWidget(Dialog)
        self.Suplierlist.setGeometry(QtCore.QRect(5, 71, 391, 321))
        self.Suplierlist.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Suplierlist.setAlternatingRowColors(False)
        self.Suplierlist.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.Suplierlist.setFlow(QtWidgets.QListView.TopToBottom)
        self.Suplierlist.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.Suplierlist.setViewMode(QtWidgets.QListView.ListMode)
        self.Suplierlist.setModelColumn(0)
        self.Suplierlist.setObjectName("Suplierlist")
        self.before_date = QtWidgets.QDateEdit(Dialog)
        self.before_date.setGeometry(QtCore.QRect(0, 20, 121, 21))
        self.before_date.setMaximumSize(QtCore.QSize(121, 16777215))
        self.before_date.setObjectName("before_date")
        self.after_date = QtWidgets.QDateEdit(Dialog)
        self.after_date.setGeometry(QtCore.QRect(180, 20, 121, 22))
        self.after_date.setObjectName("after_date")
        self.Accountlist = QtWidgets.QListWidget(Dialog)
        self.Accountlist.setGeometry(QtCore.QRect(400, 190, 151, 201))
        self.Accountlist.setObjectName("Accountlist")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 40, 306, 275))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.calendar1 = QtWidgets.QCalendarWidget(self.verticalLayoutWidget_2)
        self.calendar1.setGridVisible(True)
        self.calendar1.setSelectionMode(QtWidgets.QCalendarWidget.SingleSelection)
        self.calendar1.setNavigationBarVisible(True)
        self.calendar1.setObjectName("calendar1")
        self.verticalLayout_2.addWidget(self.calendar1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.calendar_yes_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.calendar_yes_button.setDefault(False)
        self.calendar_yes_button.setFlat(False)
        self.calendar_yes_button.setObjectName("calendar_yes_button")
        self.horizontalLayout.addWidget(self.calendar_yes_button)
        self.calendar_cancal_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.calendar_cancal_button.setObjectName("calendar_cancal_button")
        self.horizontalLayout.addWidget(self.calendar_cancal_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.export_button.setText(_translate("Dialog", "导出"))
        self.select_all_button.setText(_translate("Dialog", "全选"))
        self.clear_all_button.setText(_translate("Dialog", "全清"))
        self.close_button.setText(_translate("Dialog", "关闭"))
        self.Suplierlist.setSortingEnabled(True)
        self.Accountlist.setSortingEnabled(True)
        self.calendar_yes_button.setText(_translate("Dialog", "确定"))
        self.calendar_cancal_button.setText(_translate("Dialog", "取消"))
