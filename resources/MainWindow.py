# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\asus\coding\python\osu_player\resources\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(560, 775)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.song_info_label = QtWidgets.QLabel(self.centralwidget)
        self.song_info_label.setText("")
        self.song_info_label.setObjectName("song_info_label")
        self.verticalLayout.addWidget(self.song_info_label)
        self.song_progress_slider = QtWidgets.QSlider(self.centralwidget)
        self.song_progress_slider.setOrientation(QtCore.Qt.Horizontal)
        self.song_progress_slider.setObjectName("song_progress_slider")
        self.verticalLayout.addWidget(self.song_progress_slider)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stop_resume_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.stop_resume_pushbutton.setEnabled(True)
        self.stop_resume_pushbutton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\Users\\asus\\coding\\python\\osu_player\\resources\\play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_resume_pushbutton.setIcon(icon)
        self.stop_resume_pushbutton.setObjectName("stop_resume_pushbutton")
        self.horizontalLayout.addWidget(self.stop_resume_pushbutton)
        self.former_song_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.former_song_pushbutton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:\\Users\\asus\\coding\\python\\osu_player\\resources\\former.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.former_song_pushbutton.setIcon(icon1)
        self.former_song_pushbutton.setObjectName("former_song_pushbutton")
        self.horizontalLayout.addWidget(self.former_song_pushbutton)
        self.next_song_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.next_song_pushbutton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("C:\\Users\\asus\\coding\\python\\osu_player\\resources\\next.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next_song_pushbutton.setIcon(icon2)
        self.next_song_pushbutton.setObjectName("next_song_pushbutton")
        self.horizontalLayout.addWidget(self.next_song_pushbutton)
        self.play_mode_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.play_mode_pushbutton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("C:\\Users\\asus\\coding\\python\\osu_player\\resources\\random.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_mode_pushbutton.setIcon(icon3)
        self.play_mode_pushbutton.setObjectName("play_mode_pushbutton")
        self.horizontalLayout.addWidget(self.play_mode_pushbutton)
        self.menu_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.menu_pushbutton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("C:\\Users\\asus\\coding\\python\\osu_player\\resources\\menu.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu_pushbutton.setIcon(icon4)
        self.menu_pushbutton.setObjectName("menu_pushbutton")
        self.horizontalLayout.addWidget(self.menu_pushbutton)
        self.sort_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.sort_combobox.setObjectName("sort_combobox")
        self.sort_combobox.addItem("")
        self.sort_combobox.addItem("")
        self.sort_combobox.addItem("")
        self.sort_combobox.addItem("")
        self.horizontalLayout.addWidget(self.sort_combobox)
        self.sort_direction_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.sort_direction_pushbutton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("C:\\Users\\asus\\coding\\python\\osu_player\\resources\\up.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sort_direction_pushbutton.setIcon(icon5)
        self.sort_direction_pushbutton.setObjectName("sort_direction_pushbutton")
        self.horizontalLayout.addWidget(self.sort_direction_pushbutton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.mute_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.mute_pushbutton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("C:\\Users\\asus\\coding\\python\\osu_player\\resources\\volume2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mute_pushbutton.setIcon(icon6)
        self.mute_pushbutton.setObjectName("mute_pushbutton")
        self.horizontalLayout.addWidget(self.mute_pushbutton)
        self.volume_slider = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volume_slider.sizePolicy().hasHeightForWidth())
        self.volume_slider.setSizePolicy(sizePolicy)
        self.volume_slider.setOrientation(QtCore.Qt.Horizontal)
        self.volume_slider.setObjectName("volume_slider")
        self.horizontalLayout.addWidget(self.volume_slider)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.search_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_lineedit.setObjectName("search_lineedit")
        self.verticalLayout.addWidget(self.search_lineedit)
        self.beatmapitem_listwidget = QtWidgets.QListWidget(self.centralwidget)
        self.beatmapitem_listwidget.setObjectName("beatmapitem_listwidget")
        self.verticalLayout.addWidget(self.beatmapitem_listwidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.action_Browse = QtWidgets.QAction(MainWindow)
        self.action_Browse.setObjectName("action_Browse")
        self.action_Random_Seed = QtWidgets.QAction(MainWindow)
        self.action_Random_Seed.setObjectName("action_Random_Seed")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "osu! Player"))
        self.sort_combobox.setItemText(0, _translate("MainWindow", "Title"))
        self.sort_combobox.setItemText(1, _translate("MainWindow", "Artist"))
        self.sort_combobox.setItemText(2, _translate("MainWindow", "Time Added"))
        self.sort_combobox.setItemText(3, _translate("MainWindow", "Length"))
        self.action_Browse.setText(_translate("MainWindow", "&Browse"))
        self.action_Random_Seed.setText(_translate("MainWindow", "&Random Seed"))
