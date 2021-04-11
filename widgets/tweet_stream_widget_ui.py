# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/tweet_stream.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_TweetStream(object):
    def setupUi(self, TweetStream):
        TweetStream.setObjectName("TweetStream")
        TweetStream.resize(415, 830)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TweetStream.sizePolicy().hasHeightForWidth())
        TweetStream.setSizePolicy(sizePolicy)
        TweetStream.setMinimumSize(QtCore.QSize(415, 830))
        TweetStream.setMaximumSize(QtCore.QSize(415, 830))
        TweetStream.setAutoFillBackground(False)
        self.layoutWidget = QtWidgets.QWidget(TweetStream)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 391, 815))
        self.layoutWidget.setObjectName("layoutWidget")
        self.mainLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.mainLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setObjectName("mainLayout")
        self.tweetStream = QtWidgets.QWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tweetStream.sizePolicy().hasHeightForWidth())
        self.tweetStream.setSizePolicy(sizePolicy)
        self.tweetStream.setMinimumSize(QtCore.QSize(0, 600))
        self.tweetStream.setMaximumSize(QtCore.QSize(16777215, 600))
        self.tweetStream.setObjectName("tweetStream")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tweetStream)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tweetStreamScrollArea = QtWidgets.QScrollArea(self.tweetStream)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tweetStreamScrollArea.sizePolicy().hasHeightForWidth())
        self.tweetStreamScrollArea.setSizePolicy(sizePolicy)
        self.tweetStreamScrollArea.setWidgetResizable(True)
        self.tweetStreamScrollArea.setObjectName("tweetStreamScrollArea")
        self.tweetStreamScrollAreaContents = QtWidgets.QWidget()
        self.tweetStreamScrollAreaContents.setGeometry(QtCore.QRect(0, 0, 351, 580))
        self.tweetStreamScrollAreaContents.setObjectName("tweetStreamScrollAreaContents")
        self.tweetStreamScrollArea.setWidget(self.tweetStreamScrollAreaContents)
        self.verticalLayout_3.addWidget(self.tweetStreamScrollArea)
        self.mainLayout.addWidget(self.tweetStream)
        self.followingInfluencers = QtWidgets.QWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.followingInfluencers.sizePolicy().hasHeightForWidth())
        self.followingInfluencers.setSizePolicy(sizePolicy)
        self.followingInfluencers.setMinimumSize(QtCore.QSize(0, 125))
        self.followingInfluencers.setMaximumSize(QtCore.QSize(16777215, 125))
        self.followingInfluencers.setBaseSize(QtCore.QSize(0, 100))
        self.followingInfluencers.setObjectName("followingInfluencers")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.followingInfluencers)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.followingInfluencersScrollArea = QtWidgets.QScrollArea(self.followingInfluencers)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.followingInfluencersScrollArea.sizePolicy().hasHeightForWidth())
        self.followingInfluencersScrollArea.setSizePolicy(sizePolicy)
        self.followingInfluencersScrollArea.setMinimumSize(QtCore.QSize(0, 90))
        self.followingInfluencersScrollArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.followingInfluencersScrollArea.setWidgetResizable(True)
        self.followingInfluencersScrollArea.setObjectName("followingInfluencersScrollArea")
        self.influencers = QtWidgets.QWidget()
        self.influencers.setGeometry(QtCore.QRect(0, 0, 349, 103))
        self.influencers.setObjectName("influencers")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.influencers)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.followingInfluencersScrollArea.setWidget(self.influencers)
        self.verticalLayout.addWidget(self.followingInfluencersScrollArea)
        self.mainLayout.addWidget(self.followingInfluencers)
        self.influencerForm = QtWidgets.QWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.influencerForm.sizePolicy().hasHeightForWidth())
        self.influencerForm.setSizePolicy(sizePolicy)
        self.influencerForm.setMinimumSize(QtCore.QSize(0, 50))
        self.influencerForm.setMaximumSize(QtCore.QSize(16777215, 50))
        self.influencerForm.setObjectName("influencerForm")
        self.layoutWidget1 = QtWidgets.QWidget(self.influencerForm)
        self.layoutWidget1.setGeometry(QtCore.QRect(-20, 10, 404, 29))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.influencerFormLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.influencerFormLayout.setContentsMargins(0, 0, 0, 0)
        self.influencerFormLayout.setObjectName("influencerFormLayout")
        self.lineEditTwitterHandle = QtWidgets.QLineEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditTwitterHandle.sizePolicy().hasHeightForWidth())
        self.lineEditTwitterHandle.setSizePolicy(sizePolicy)
        self.lineEditTwitterHandle.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEditTwitterHandle.setFont(font)
        self.lineEditTwitterHandle.setText("")
        self.lineEditTwitterHandle.setMaxLength(16)
        self.lineEditTwitterHandle.setCursorPosition(0)
        self.lineEditTwitterHandle.setObjectName("lineEditTwitterHandle")
        self.influencerFormLayout.addWidget(self.lineEditTwitterHandle)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.influencerFormLayout.addItem(spacerItem)
        self.followInfluencerBtn = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.followInfluencerBtn.sizePolicy().hasHeightForWidth())
        self.followInfluencerBtn.setSizePolicy(sizePolicy)
        self.followInfluencerBtn.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.followInfluencerBtn.setFont(font)
        self.followInfluencerBtn.setObjectName("followInfluencerBtn")
        self.influencerFormLayout.addWidget(self.followInfluencerBtn)
        self.mainLayout.addWidget(self.influencerForm)

        self.retranslateUi(TweetStream)
        QtCore.QMetaObject.connectSlotsByName(TweetStream)

    def retranslateUi(self, TweetStream):
        _translate = QtCore.QCoreApplication.translate
        TweetStream.setWindowTitle(_translate("TweetStream", "Tweet Stream"))
        self.lineEditTwitterHandle.setPlaceholderText(_translate("TweetStream", "@twitterHandle"))
        self.followInfluencerBtn.setText(_translate("TweetStream", "Follow"))

