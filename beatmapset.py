import os
import re

import beatmap
from pydub import AudioSegment
import eyed3

eyed3.core.log.disabled = True


def is_valid_beatmapset(path):
    all_files = os.listdir(path)
    for file in all_files:
        if file.endswith(r'.osu'):
            return True
    return False


def cat_str_with_len_bound(str_list, length=50):
    str_out = ''
    line = ''
    for str_item in str_list:
        if len(line) + len(str_item) > length:
            str_out += line + '\n\t'
            line = ''
        line += str_item + ' '
    str_out += line
    return str_out


class BeatmapSet:
    def __init__(self, path):
        self.path = path
        self.beatmap_list = []
        self.meta_dict = {}
        self.audio_path = None
        self.title = None
        self.title_unicode = None
        self.artist = None
        self.artist_unicode = None
        self.name_unicode = None
        self.name = None
        self.source = ''
        self.tags = ''
        self.time_added = os.stat(self.path).st_atime
        self.length = 0
        all_files = os.listdir(self.path)
        for file in all_files:
            if file.endswith(r'.osu'):
                self.beatmap_list.append(beatmap.Beatmap(os.path.join(self.path, file)))
        # for b in self.beatmap_list:
        #     print(b.meta_dict)
        for category in ['General', 'Metadata']:
            for _beatmap in self.beatmap_list:
                category_dict = _beatmap[category]
                if category_dict is not None:
                    # find the first
                    # assume all beatmaps in a same beatmapset have same meta and general info
                    self.meta_dict[category] = category_dict
                    break
        self.meta_dict['Events'] = []
        for _beatmap in self.beatmap_list:
            bg_video_events = _beatmap['Events']
            if bg_video_events is not None:
                self.meta_dict['Events'].append(bg_video_events)
        _general = self.meta_dict['General']
        if 'AudioFilename' in _general:
            self.audio_path = os.path.join(self.path, _general['AudioFilename'])
            if os.path.exists(self.audio_path):
                audio_file = eyed3.load(self.audio_path)
                if audio_file is not None and audio_file.info is not None:
                    self.length = audio_file.info.time_secs * 1000
                else:
                    m = re.match(r'.*\.(.*)', self.audio_path)
                    if m is not None:
                        fmt = m.groups()[-1]
                        self.length = len(AudioSegment.from_file(self.audio_path, fmt))
        _metadata = self.meta_dict['Metadata']
        if 'Title' in _metadata:
            self.title = _metadata['Title']
        if 'TitleUnicode' in _metadata:
            self.title_unicode = _metadata['TitleUnicode']
        if 'Artist' in _metadata:
            self.artist = _metadata['Artist']
        if 'ArtistUnicode' in _metadata:
            self.artist_unicode = _metadata['ArtistUnicode']
        if 'Source' in _metadata:
            self.source = _metadata['Source']
        if 'Tags' in _metadata:
            self.tags = _metadata['Tags']
        if self.artist_unicode is not None and self.title_unicode is not None:
            self.name_unicode = self.artist_unicode + ' - ' + self.title_unicode
        if self.artist is not None and self.title is not None:
            self.name = self.artist + ' - ' + self.title
        if self.name is not None and self.name_unicode is None:
            self.name_unicode = self.name
        if self.name is None and self.name_unicode is not None:
            self.name = self.name_unicode
        if self.name is None and self.name_unicode is None:
            # try to get name from path
            m = re.match(r'\d* (.*)', os.path.basename(self.path))
            if m is not None:
                self.name = m.groups()[0]
            else:
                self.name = ''
            self.name_unicode = self.name
        if self.title_unicode is None and self.title is not None:
            self.title_unicode = self.title
        if self.title_unicode is not None and self.title is None:
            self.title = self.title_unicode
        if self.title_unicode is None and self.title is None:
            self.title = ''
            self.title_unicode = ''
        if self.artist_unicode is None and self.artist is not None:
            self.artist_unicode = self.artist
        if self.artist_unicode is not None and self.artist is None:
            self.artist = self.artist_unicode
        if self.artist_unicode is None and self.artist is None:
            self.artist = ''
            self.artist_unicode = ''
        self.bg_path_list = []
        self.video_path_list = []
        for bg_video_events in self.meta_dict['Events']:
            for event in bg_video_events:
                if event[0] == 'Video' and event[2] not in self.video_path_list:
                    self.video_path_list.append(event[2])
                elif event[0] == '0' and event[2] not in self.bg_path_list:
                    self.bg_path_list.append(event[2])
        self.video_path_list = [os.path.join(self.path, p) for p in self.video_path_list]
        self.bg_path_list = [os.path.join(self.path, p) for p in self.bg_path_list]

    def __str__(self):
        tags = self.tags.split(' ')
        tags_str = cat_str_with_len_bound(tags)
        return self.title_unicode + \
               '\nArtist: \t' + self.artist_unicode + \
               '\nSource: \t' + self.source + \
               '\nTags: \t[' + tags_str + ']'

    def unicode_info(self):
        return self.title_unicode + \
               '\nArtist: ' + self.artist_unicode + \
               '\nSource: ' + self.source + \
               '\nTags: ' + self.tags

    def ascii_info(self):
        return self.title + \
               '\nArtist: ' + self.artist + \
               '\nSource: ' + self.source + \
               '\nTags: ' + self.tags
