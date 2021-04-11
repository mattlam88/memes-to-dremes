# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/influencer_template.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Influencer(object):
    def setupUi(self, Influencer):
        Influencer.setObjectName("Influencer")
        Influencer.resize(181, 45)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Influencer.sizePolicy().hasHeightForWidth())
        Influencer.setSizePolicy(sizePolicy)
        Influencer.setMinimumSize(QtCore.QSize(0, 0))
        Influencer.setMaximumSize(QtCore.QSize(181, 45))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Influencer)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.unfollowBtn = QtWidgets.QPushButton(Influencer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.unfollowBtn.sizePolicy().hasHeightForWidth())
        self.unfollowBtn.setSizePolicy(sizePolicy)
        self.unfollowBtn.setMaximumSize(QtCore.QSize(25, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.unfollowBtn.setFont(font)
        self.unfollowBtn.setObjectName("unfollowBtn")
        self.horizontalLayout.addWidget(self.unfollowBtn)
        self.twitterHandle = QtWidgets.QLabel(Influencer)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.twitterHandle.setFont(font)
        self.twitterHandle.setObjectName("twitterHandle")
        self.horizontalLayout.addWidget(self.twitterHandle)

        self.retranslateUi(Influencer)
        QtCore.QMetaObject.connectSlotsByName(Influencer)

    def retranslateUi(self, Influencer):
        _translate = QtCore.QCoreApplication.translate
        Influencer.setWindowTitle(_translate("Influencer", "Form"))
        self.unfollowBtn.setText(_translate("Influencer", "X"))
        self.twitterHandle.setText(_translate("Influencer", "@abcdefghijklmno"))


