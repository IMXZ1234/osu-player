import re

from PyQt5 import QtCore, QtGui, QtWidgets


class DialogSetting(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DialogSetting, self).__init__(parent)
        self.setupUi(self)
        self.connect_slots()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 310)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ignore_case_checkbox = QtWidgets.QCheckBox(Dialog)
        self.ignore_case_checkbox.setChecked(True)
        self.ignore_case_checkbox.setObjectName("ignore_case_checkbox")
        self.verticalLayout.addWidget(self.ignore_case_checkbox)
        self.seed_label = QtWidgets.QLabel(Dialog)
        self.seed_label.setObjectName("seed_label")
        self.verticalLayout.addWidget(self.seed_label)
        self.seed_lineedit = QtWidgets.QLineEdit(Dialog)
        self.seed_lineedit.setObjectName("seed_lineedit")
        self.verticalLayout.addWidget(self.seed_lineedit)
        self.format_label = QtWidgets.QLabel(Dialog)
        self.format_label.setObjectName("format_label")
        self.verticalLayout.addWidget(self.format_label)
        self.format_textedit = QtWidgets.QPlainTextEdit(Dialog)
        self.format_textedit.setObjectName("format_textedit")
        self.verticalLayout.addWidget(self.format_textedit)
        self.change_beatmap_dir_pushbutton = QtWidgets.QPushButton(Dialog)
        self.change_beatmap_dir_pushbutton.setObjectName("change_beatmap_dir_pushbutton")
        self.verticalLayout.addWidget(self.change_beatmap_dir_pushbutton)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.ignore_case_checkbox.setText(_translate("Dialog", "Ignore upper/lower case in search"))
        self.seed_label.setText(_translate("Dialog", "Set random seed"))
        self.format_label.setText(_translate("Dialog", "Song info format"))
        self.format_textedit.setPlainText(_translate("Dialog", "{artist_unicode} - {title_unicode}"))
        self.change_beatmap_dir_pushbutton.setText(_translate("Dialog", "Browse Songs directory"))

    def connect_slots(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.change_beatmap_dir_pushbutton.clicked.connect(self.on_change_beatmap_dir_pushbutton_clicked)

    def on_change_beatmap_dir_pushbutton_clicked(self):
        _dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Find out osu! Songs Directory')
        if _dir is not None:
            self.parent().set_beatmap_dir(_dir)

    def accept(self) -> None:
        if self.seed_lineedit.text() == '':
            random_seed = None
        else:
            try:
                random_seed = int(self.seed_lineedit.text())
            except ValueError:
                QtWidgets.QMessageBox(parent=self, text='Invalid seed! Seed should be int!')
                return
        # check song format string validity
        try:
            song_format = self.format_textedit.toPlainText()
            song_format.format(**{'title': '', 'title_unicode': '',
                                  'artist': '', 'artist_unicode': '',
                                  'source': '', 'tags': '', })
        except KeyError:
            QtWidgets.QMessageBox(parent=self, text='Invalid song format!')
            return
        if self.ignore_case_checkbox.isChecked() != self.parent().ignore_case:
            self.parent().ignore_case = self.ignore_case_checkbox.isChecked()
        self.parent().set_random_seed(random_seed)
        self.parent().set_song_format(song_format)
        super(DialogSetting, self).accept()
