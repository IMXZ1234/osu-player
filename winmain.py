import os
import random
import sys
from PyQt5 import QtWidgets, QtCore, QtGui

import beatmapset
import dialogsetting
import playthread

MODE_ORDERED = 0
MODE_RANDOM = 1
SORT_TITLE = 0
SORT_ARTIST = 1
SORT_TIME_ADDED = 2
SORT_LENGTH = 3


def get_random_order(list_len):
    """
    Ensures ith item is not i itself.

    :param list_len:
    :return:
    """
    order = list(range(list_len))
    random.shuffle(order)
    for i in range(list_len):
        if order[i] == i:
            if i == list_len - 1:
                order[i], order[0] = order[0], order[i]
                return order
            order[i], order[i + 1] = order[i + 1], order[i]
    return order


class WinMain(QtWidgets.QMainWindow):
    def __init__(self):
        super(WinMain, self).__init__()
        self.cwd = os.getcwd()
        self.resource_dir = os.path.join(self.cwd, 'resources')
        self.resource_dict = {
            'icon_former': QtGui.QIcon(os.path.join(self.resource_dir, 'former.svg')),
            'icon_mute': QtGui.QIcon(os.path.join(self.resource_dir, 'mute.svg')),
            'icon_next': QtGui.QIcon(os.path.join(self.resource_dir, 'next.svg')),
            'icon_ordered': QtGui.QIcon(os.path.join(self.resource_dir, 'ordered.svg')),
            'icon_pause': QtGui.QIcon(os.path.join(self.resource_dir, 'pause.svg')),
            'icon_play': QtGui.QIcon(os.path.join(self.resource_dir, 'play.svg')),
            'icon_random': QtGui.QIcon(os.path.join(self.resource_dir, 'random.svg')),
            'icon_volume1': QtGui.QIcon(os.path.join(self.resource_dir, 'volume1.svg')),
            'icon_volume2': QtGui.QIcon(os.path.join(self.resource_dir, 'volume2.svg')),
            'icon_menu': QtGui.QIcon(os.path.join(self.resource_dir, 'menu.svg')),
            'icon_up': QtGui.QIcon(os.path.join(self.resource_dir, 'up.svg')),
            'icon_down': QtGui.QIcon(os.path.join(self.resource_dir, 'down.svg')),
        }
        self.setupUi(self)
        # self.song_list_widget = QtWidgets.QListWidget(self)
        # self.change_dir_button = QtWidgets.QPushButton('&Browse', self)
        self.ignore_case = True
        self.random_seed = None
        self.song_format = '{artist_unicode} - {title_unicode}'
        self.beatmap_dir = ''
        self.beatmapset_list = []
        self.set_beatmap_dir(r'C:\Users\asus\AppData\Local\osu!\Songs')
        self.paused = True
        self.start_paused = False
        # current idx in beatmapset_list
        self.current_idx = 0
        self.current_volume = 100
        self.muted = False
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.mute_pushbutton.setIcon(self.resource_dict['icon_volume2'])
        # if self.current_volume <= 50:
        #     self.mute_pushbutton.setIcon(self.resource_dict['icon_volume1'])
        # else:
        #     self.mute_pushbutton.setIcon(self.resource_dict['icon_volume2'])
        self.mode = MODE_RANDOM
        self.play_order = get_random_order(len(self.beatmapset_list))
        self.reverse_play_order = [0 for _ in range(len(self.play_order))]
        for i in range(len(self.play_order)):
            self.reverse_play_order[self.play_order[i]] = self.play_order[i]
        self.play_thread = playthread.PlayThread(self)
        self.connect_slots()
        # 0: a-z
        self.sort_direction = SORT_TITLE
        # maps index of items in beatmapitem_listwidget to index in beatmapset_list
        self.sort_item_index_list = list(range(len(self.beatmapset_list)))
        self.search_item_index_list = self.sort_item_index_list.copy()
        self.on_sort_combobox_currentIndexChanged()
        self.setting_dialog = dialogsetting.DialogSetting(self)
        if len(self.beatmapset_list) != 0:
            self.play(self.beatmapset_list[self.current_idx], start_paused=True)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(560, 775)
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
        self.stop_resume_pushbutton.setObjectName("stop_resume_pushbutton")
        self.horizontalLayout.addWidget(self.stop_resume_pushbutton)
        self.former_song_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.former_song_pushbutton.setText("")
        self.former_song_pushbutton.setObjectName("former_song_pushbutton")
        self.horizontalLayout.addWidget(self.former_song_pushbutton)
        self.next_song_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.next_song_pushbutton.setText("")
        self.next_song_pushbutton.setObjectName("next_song_pushbutton")
        self.horizontalLayout.addWidget(self.next_song_pushbutton)
        self.play_mode_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.play_mode_pushbutton.setText("")
        self.play_mode_pushbutton.setObjectName("play_mode_pushbutton")
        self.horizontalLayout.addWidget(self.play_mode_pushbutton)
        self.menu_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.menu_pushbutton.setText("")
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
        self.sort_direction_pushbutton.setObjectName("sort_direction_pushbutton")
        self.horizontalLayout.addWidget(self.sort_direction_pushbutton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.mute_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.mute_pushbutton.setText("")
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
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "osu! Player"))
        self.song_info_label.setText(_translate("MainWindow", ""))
        self.stop_resume_pushbutton.setIcon(self.resource_dict['icon_play'])
        self.former_song_pushbutton.setIcon(self.resource_dict['icon_former'])
        self.next_song_pushbutton.setIcon(self.resource_dict['icon_next'])
        self.play_mode_pushbutton.setIcon(self.resource_dict['icon_random'])
        self.menu_pushbutton.setIcon(self.resource_dict['icon_menu'])
        self.sort_direction_pushbutton.setIcon(self.resource_dict['icon_up'])
        self.mute_pushbutton.setIcon(self.resource_dict['icon_volume2'])
        self.sort_combobox.setItemText(SORT_TITLE, _translate("MainWindow", "Title"))
        self.sort_combobox.setItemText(SORT_ARTIST, _translate("MainWindow", "Artist"))
        self.sort_combobox.setItemText(SORT_TIME_ADDED, _translate("MainWindow", "Time Added"))
        self.sort_combobox.setItemText(SORT_LENGTH, _translate("MainWindow", "Length"))
        self.search_lineedit.setText(_translate("MainWindow", ""))  # Type Here to Search

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.play_thread.stop()
        self.play_thread.wait(10)
        super(WinMain, self).closeEvent(a0)

    def on_search_lineedit_textEdited(self, text):
        self.update_search_item_index_list(text)

    def on_beatmapset_listwidget_currentItemChanged(self, item):
        self.current_idx = self.beatmapitem_listwidget.indexFromItem(item).row()
        self.play(self.beatmapset_list[self.search_item_index_list[self.current_idx]], self.start_paused)

    def on_menu_pushbutton_clicked(self, checked):
        self.setting_dialog.show()

    def on_stop_resume_pushbutton_clicked(self):
        if self.paused:
            self.paused = False
            self.stop_resume_pushbutton.setIcon(self.resource_dict['icon_pause'])
            self.play_thread.resume()
        else:
            self.paused = True
            self.stop_resume_pushbutton.setIcon(self.resource_dict['icon_play'])
            self.play_thread.pause()

    def on_play_mode_pushbutton_clicked(self):
        if self.mode == MODE_RANDOM:
            self.mode = MODE_ORDERED
            self.play_mode_pushbutton.setIcon(self.resource_dict['icon_ordered'])
        else:
            self.mode = MODE_RANDOM
            self.play_mode_pushbutton.setIcon(self.resource_dict['icon_random'])
        self.gen_play_order(len(self.beatmapset_list))

    def on_mute_pushbutton_clicked(self):
        if self.muted:
            self.muted = False
            if self.current_volume <= 50:
                self.mute_pushbutton.setIcon(self.resource_dict['icon_volume1'])
            else:
                self.mute_pushbutton.setIcon(self.resource_dict['icon_volume2'])
            self.play_thread.adjust_volume(self.current_volume / self.volume_slider.maximum())
        else:
            self.muted = True
            self.mute_pushbutton.setIcon(self.resource_dict['icon_mute'])
            self.play_thread.mute()

    def on_former_song_pushbutton_clicked(self):
        self.current_idx = self.reverse_play_order[self.current_idx]
        self.sel_and_show_beatmapset(self.current_idx)
        self.play(self.beatmapset_list[self.sort_item_index_list[self.current_idx]], self.start_paused)

    def on_next_song_pushbutton_clicked(self):
        self.current_idx = self.play_order[self.current_idx]
        self.sel_and_show_beatmapset(self.current_idx)
        self.play(self.beatmapset_list[self.sort_item_index_list[self.current_idx]], self.start_paused)

    def on_sort_direction_pushbutton(self):
        self.sort_direction = 1 - self.sort_direction
        if self.sort_direction == 0:
            self.sort_direction_pushbutton.setIcon(self.resource_dict['icon_up'])
        else:
            self.sort_direction_pushbutton.setIcon(self.resource_dict['icon_down'])
        self.sort_item_index_list.reverse()
        self.update_search_item_index_list(self.search_lineedit.text())
        self.update_song_list(self.search_item_index_list)
        self.sel_and_show_beatmapset(self.current_idx)

    def on_sort_combobox_currentIndexChanged(self):
        self.sort()
        self.update_search_item_index_list(self.search_lineedit.text())
        self.update_song_list(self.search_item_index_list)
        self.sel_and_show_beatmapset(self.current_idx)

    def on_song_progress_slider_valueChanged(self, value):
        self.play_thread.set_to_frame(value)

    def on_volume_slider_valueChanged(self, value):
        if not self.volume_slider.isSliderDown():
            self.set_volume(value)

    def on_play_over(self, terminated):
        # print('on_play_over')
        if not terminated:
            # print('not terminated')
            self.current_idx = self.play_order[self.current_idx]
            self.sel_and_show_beatmapset(self.current_idx)
            self.play(self.beatmapset_list[self.sort_item_index_list[self.current_idx]], self.start_paused)

    def on_frame_played(self, index):
        self.song_progress_slider.valueChanged.disconnect()
        self.song_progress_slider.setValue(index)
        self.song_progress_slider.valueChanged.connect(self.on_song_progress_slider_valueChanged)
        # print(index)

    def connect_slots(self):
        self.beatmapitem_listwidget.currentItemChanged.connect(self.on_beatmapset_listwidget_currentItemChanged)
        self.menu_pushbutton.clicked.connect(self.on_menu_pushbutton_clicked)
        self.stop_resume_pushbutton.clicked.connect(self.on_stop_resume_pushbutton_clicked)
        self.play_mode_pushbutton.clicked.connect(self.on_play_mode_pushbutton_clicked)
        self.mute_pushbutton.clicked.connect(self.on_mute_pushbutton_clicked)
        self.next_song_pushbutton.clicked.connect(self.on_next_song_pushbutton_clicked)
        self.former_song_pushbutton.clicked.connect(self.on_former_song_pushbutton_clicked)
        self.sort_direction_pushbutton.clicked.connect(self.on_sort_direction_pushbutton)
        self.sort_combobox.currentIndexChanged.connect(self.on_sort_combobox_currentIndexChanged)
        self.song_progress_slider.valueChanged.connect(self.on_song_progress_slider_valueChanged)
        self.song_progress_slider.sliderPressed.connect(lambda: self.play_thread.pause())
        self.song_progress_slider.sliderReleased.connect(lambda: self.play_thread.resume())
        self.volume_slider.valueChanged.connect(self.on_volume_slider_valueChanged)
        # self.volume_slider.sliderPressed.connect(self.on_volume_slider_sliderPressed)
        self.volume_slider.sliderReleased.connect(lambda: self.set_volume(self.volume_slider.value()))
        self.play_thread.play_over.connect(self.on_play_over)
        self.play_thread.frame_played.connect(self.on_frame_played)
        self.search_lineedit.textEdited.connect(self.on_search_lineedit_textEdited)

    def set_beatmap_dir(self, s):
        if not os.path.exists(s):
            return
        if s == self.beatmap_dir:
            return
        self.beatmap_dir = s
        self.beatmapset_list.clear()
        for d in os.listdir(s):
            beatmapset_path = os.path.join(s, d)
            if not beatmapset.is_valid_beatmapset(beatmapset_path):
                continue
            _beatmapset = beatmapset.BeatmapSet(beatmapset_path)
            self.beatmapset_list.append(_beatmapset)

    def update_song_list(self, item_index_list):
        self.beatmapitem_listwidget.currentItemChanged.disconnect(self.on_beatmapset_listwidget_currentItemChanged)
        self.beatmapitem_listwidget.clear()
        self.beatmapitem_listwidget.currentItemChanged.connect(self.on_beatmapset_listwidget_currentItemChanged)
        for index in item_index_list:
            _beatmapset = self.beatmapset_list[index]
            item_str = self.song_format.format(**{'title': _beatmapset.title,
                                                  'title_unicode': _beatmapset.title_unicode,
                                                  'artist': _beatmapset.artist,
                                                  'artist_unicode': _beatmapset.artist_unicode,
                                                  'source': _beatmapset.source,
                                                  'tags': _beatmapset.tags, })
            self.beatmapitem_listwidget.addItem(item_str)

    def sort(self):
        zip_list = [(i, self.beatmapset_list[i]) for i in range(len(self.beatmapset_list))]
        sort_key = self.sort_combobox.currentIndex()
        if sort_key == SORT_TITLE:
            key_func = lambda item: item[1].title if item[1].title is not None else ''
        elif sort_key == SORT_ARTIST:
            key_func = lambda item: item[1].artist if item[1].artist is not None else ''
        elif sort_key == SORT_TIME_ADDED:
            key_func = lambda item: item[1].time_added
        elif sort_key == SORT_LENGTH:
            key_func = lambda item: item[1].length
        else:
            key_func = lambda item: item[0]
        zip_list.sort(key=key_func)
        self.sort_item_index_list = [item[0] for item in zip_list]

    def gen_play_order(self, length):
        if self.mode == MODE_RANDOM:
            self.mode = MODE_ORDERED
            self.play_order = list(range(1, length + 1))
            self.play_order[-1] = 0
            self.reverse_play_order = [length - 1]
            self.reverse_play_order.extend(list(range(length - 1)))
        else:
            self.mode = MODE_RANDOM
            self.play_order = get_random_order(length)
            self.reverse_play_order = [0 for _ in range(length)]
            for i in range(len(self.play_order)):
                self.reverse_play_order[self.play_order[i]] = self.play_order[i]

    def update_search_item_index_list(self, text):
        if text == '':
            self.search_item_index_list = self.sort_item_index_list.copy()
        else:
            search_artist = False
            search_source = False
            search_tags = False
            if text.startswith('@'):
                text = text[1:]
                search_artist = True
            elif text.startswith('#'):
                text = text[1:]
                search_source = True
            elif text.startswith('$'):
                text = text[1:]
                search_tags = True
            if self.ignore_case:
                text = text.lower()
            pos_beatmapset_list = []
            for i in self.sort_item_index_list:
                if search_artist:
                    property = self.beatmapset_list[i].artist
                elif search_source:
                    property = self.beatmapset_list[i].source
                elif search_tags:
                    property = self.beatmapset_list[i].tags
                else:
                    property = self.beatmapset_list[i].title
                if self.ignore_case:
                    property = property.lower()
                pos = property.find(text)
                if pos != -1:
                    if pos >= len(pos_beatmapset_list):
                        while len(pos_beatmapset_list) <= pos:
                            pos_beatmapset_list.append([])
                    pos_beatmapset_list[pos].append(i)
            self.search_item_index_list.clear()
            for beatmapset_list in pos_beatmapset_list:
                self.search_item_index_list.extend(beatmapset_list)
        self.update_song_list(self.search_item_index_list)

    def sel_and_show_beatmapset(self, idx):
        if idx not in self.search_item_index_list:
            return
        self.beatmapitem_listwidget.currentItemChanged.disconnect(self.on_beatmapset_listwidget_currentItemChanged)
        item = self.beatmapitem_listwidget.itemAt(self.search_item_index_list.index(idx), 0)
        self.beatmapitem_listwidget.setCurrentItem(item)
        self.beatmapitem_listwidget.scrollToItem(item)
        self.beatmapitem_listwidget.currentItemChanged.connect(self.on_beatmapset_listwidget_currentItemChanged)

    def play(self, item, start_paused=False):
        if self.play_thread.isRunning():
            self.play_thread.stop()
            self.play_thread.wait()
        if start_paused:
            self.paused = True
            self.stop_resume_pushbutton.setIcon(self.resource_dict['icon_play'])
        else:
            self.paused = False
            self.stop_resume_pushbutton.setIcon(self.resource_dict['icon_pause'])
        self.play_thread.set_play_item(item, start_paused, self.current_volume / 100)
        self.song_info_label.setText(str(item))
        self.song_progress_slider.setMaximum(self.play_thread.frame_count - 1)
        self.play_thread.start()

    def set_volume(self, value):
        self.current_volume = value
        if self.current_volume == 0:
            self.mute_pushbutton.setIcon(self.resource_dict['icon_mute'])
        elif self.current_volume <= 50:
            self.mute_pushbutton.setIcon(self.resource_dict['icon_volume1'])
        else:
            self.mute_pushbutton.setIcon(self.resource_dict['icon_volume2'])
        self.play_thread.adjust_volume(value / self.volume_slider.maximum())

    def set_random_seed(self, random_seed):
        self.random_seed = random_seed
        random.seed(self.random_seed)
        self.gen_play_order(len(self.beatmapset_list))

    def set_song_format(self, song_format):
        self.song_format = song_format
        self.update_song_list(self.search_item_index_list)


if __name__ == '__main__':
    # a = '[00asd]'
    # print('a' < 'Ads')
    # a.split()
    # m = re.match(r'\[(.+)]', a)
    # print(m.group())
    # print(os.stat('./beatmap.py').st_atime)
    # import time
    # print(time.time())
    # a = '{ab}c'.format(**{'ab':'0', 'df':'45'})
    # print(a)
    app = QtWidgets.QApplication([])
    win = WinMain()
    win.show()
    sys.exit(app.exec())
