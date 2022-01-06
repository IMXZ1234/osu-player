import os
import re


def retrieve_category_data(f, category):
    line = f.readline().replace(' : ', ':').replace(': ', ':')
    if category in ['General', 'Metadata']:
        category_dict = {}
        m = re.match(r'(.*):(.*)', line[:-1])
        while m is not None:
            # g = m.groups()
            split = line[:-1].split(':')
            category_dict[split[0]] = str.join(':', split[1:])
            line = f.readline().replace(' : ', ':').replace(': ', ':')
            m = re.match(r'(.*):(.*)', line[:-1])
        return category_dict, line
    elif category in ['Events']:
        events = []
        while line.startswith('//'):
            if line[:-1] == r'//Background and Video events':
                line = f.readline()
                while not line.startswith('//'):
                    events.append(line[:-1].split(','))
                    line = f.readline()
                break
            line = f.readline()
        return events, line
    else:
        return None, line


class Beatmap:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path)
        self.meta_dict = {}
        # if not self.name.endswith(r'.osu'):
        #     print('Meta does not end with \'.osu\'!')
        # print(self.path)
        encoding_list = ['utf-8', 'utf-16']
        for encoding in encoding_list:
            try:
                with open(self.path, 'r', encoding=encoding) as f:
                    self.parse_meta(f)
                break
            except UnicodeDecodeError:
                continue

    def parse_meta(self, f):
        # exclude the trailing '\n'
        line = f.readline()
        while line != '':
            # print(line)
            m = re.match(r'\[(.+)]', line[:-1])
            if m is not None:
                category = m.groups()[0]
                category_data, line = retrieve_category_data(f, category)
                # print('category_data')
                # print(category_data)
                # print('line')
                # print(line)
                if category_data is not None:
                    self.meta_dict[category] = category_data
            else:
                line = f.readline()

    def __contains__(self, item):
        return item in self.meta_dict

    def __getitem__(self, item):
        if item in self.meta_dict:
            return self.meta_dict[item]
        else:
            return None
