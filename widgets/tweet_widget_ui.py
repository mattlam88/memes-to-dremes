# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/tweet_template.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Tweet(object):
    def setupUi(self, Tweet):
        Tweet.setObjectName("Tweet")
        Tweet.resize(320, 150)
        Tweet.setMaximumSize(QtCore.QSize(320, 150))
        self.verticalLayout = QtWidgets.QVBoxLayout(Tweet)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tweet = QtWidgets.QTextBrowser(Tweet)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tweet.sizePolicy().hasHeightForWidth())
        self.tweet.setSizePolicy(sizePolicy)
        self.tweet.setMaximumSize(QtCore.QSize(400, 800))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tweet.setFont(font)
        self.tweet.setObjectName("tweet")
        self.verticalLayout.addWidget(self.tweet)
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setObjectName("mainLayout")
        self.twitterHandle = QtWidgets.QLabel(Tweet)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.twitterHandle.setFont(font)
        self.twitterHandle.setObjectName("twitterHandle")
        self.mainLayout.addWidget(self.twitterHandle)
        self.cryptoTicker = QtWidgets.QLabel(Tweet)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cryptoTicker.setFont(font)
        self.cryptoTicker.setObjectName("cryptoTicker")
        self.mainLayout.addWidget(self.cryptoTicker)
        self.verticalLayout.addLayout(self.mainLayout)

        self.retranslateUi(Tweet)
        QtCore.QMetaObject.connectSlotsByName(Tweet)

    def retranslateUi(self, Tweet):
        _translate = QtCore.QCoreApplication.translate
        Tweet.setWindowTitle(_translate("Tweet", "Tweet Template"))
        self.tweet.setHtml(_translate("Tweet", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt;\">Sample message that will help demonstrate the character limit for a typical tweet so we know how big the box for the tweet should be. This should give you an idea of how long a tweet can be in gui format. Some more empty text because there is nothing else left to say. Okay bye!!!</span></p></body></html>"))
        self.twitterHandle.setText(_translate("Tweet", "TextLabel"))
        self.cryptoTicker.setText(_translate("Tweet", "TextLabel"))


