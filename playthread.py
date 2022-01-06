import re
import math

from PyQt5 import QtCore
from pydub import AudioSegment
import pyaudio
import array


class PlayThread(QtCore.QThread):
    play_over = QtCore.pyqtSignal(bool)
    frame_played = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(PlayThread, self).__init__(parent)
        self.p = pyaudio.PyAudio()
        self.fmt = None
        self.stream = None
        self.mutex = QtCore.QMutex()
        self.wait_con = QtCore.QWaitCondition()
        self.should_pause = False
        self.should_terminate = False
        self.ori_audio_seg = None
        self.audio_seg = None
        self.current_frame = 0
        self.frame_count = None
        self.frame_rate = None

    def set_play_item(self, item, start_paused=False, proportion=1):
        self.should_terminate = False
        print(item.audio_path)
        m = re.match(r'.*\.(.*)', item.audio_path)
        if m is None:
            print('Failed to set play item: invalid video path.')
            return False
        fmt = m.groups()[-1]
        self.ori_audio_seg = AudioSegment.from_file(item.audio_path, fmt)
        self.audio_seg = self.ori_audio_seg.apply_gain(-20 * (1 - proportion))
        self.frame_count = int(self.audio_seg.frame_count())
        if start_paused:
            self.should_pause = True

    def adjust_volume(self, proportion):
        self.audio_seg = self.ori_audio_seg.apply_gain(-20 * (1 - proportion))

    def mute(self):
        data = b"\0" * self.frame_count * int(self.ori_audio_seg.channels) * int(self.ori_audio_seg.sample_width)
        self.audio_seg = AudioSegment(data, metadata={"channels": self.ori_audio_seg.channels,
                                                      "sample_width": self.ori_audio_seg.sample_width,
                                                      "frame_rate": self.ori_audio_seg.frame_rate,
                                                      "frame_width": self.ori_audio_seg.frame_width})

    def pause(self):
        # print('pause')
        self.should_pause = True

    def resume(self):
        # print('resume')
        self.should_pause = False
        self.wait_con.wakeOne()

    def stop(self):
        self.current_frame = 0
        self.should_pause = False
        self.should_terminate = True
        self.wait_con.wakeOne()

    def set_to_frame(self, index):
        self.current_frame = min(self.frame_count - 1, index)

    def set_to_time(self, time):
        self.current_frame = math.floor(time * self.audio_seg.frame_rate)

    def run(self) -> None:
        # print('start')
        if self.p is None:
            print('Set play item first!')
            return
        self.stream = self.p.open(self.audio_seg.frame_rate, self.audio_seg.channels,
                                  self.p.get_format_from_width(self.audio_seg.sample_width),
                                  output=True)
        self.current_frame = 0
        while True:
            if self.should_pause:
                self.mutex.lock()
                # print('wait')
                self.wait_con.wait(self.mutex)
                self.mutex.unlock()
                # print('wait over')
            if self.current_frame >= self.frame_count or self.should_terminate:
                break
            data = self.audio_seg.get_frame(self.current_frame)
            self.stream.write(data)
            self.current_frame += 1
            self.frame_played.emit(self.current_frame)
        self.stream.stop_stream()
        self.stream.close()
        if self.should_terminate:
            self.play_over.emit(True)
        else:
            self.play_over.emit(False)
