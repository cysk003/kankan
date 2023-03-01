#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json

class Parser(object):
    lives = []
    new_lives = []

    def __init__(self, file) -> None:
        spit_file = os.path.splitext(file)
        self.type = spit_file[-1]
        self.file_name = spit_file[-2]
        if not os.path.isfile(file) or self.type not in ['.txt','.m3u','.m3u8']:
            raise TypeError("这不是一个文件，或者文件不存在, 或者文件格式不正确！")
        self.file = file
        self.load_data(file)

    def load_data(self, file):
        with open(file, encoding='UTF-8') as data:
            self.lives = data.readlines()

    def txt_to_m3u(self):
        self.new_lives.append('#EXTM3U\n')
        meta = '#EXTINF:-1 group-title="{}" tvg-logo="",{}\n'
        group = ''
        for line in self.lives:
            if line == "" or line == '\n': continue
            if line.endswith('#genre#\n'):
                group = line.replace(',#genre#\n', '')
                continue
            channel,url = line.split(',')
            self.new_lives.append(meta.format(group, channel))
            self.new_lives.append(url)
        return self


    def m3u_to_txt(self):
        current_group = ''
        channel = ''
        for line in self.lives:
            if line == '#EXTM3U\n': continue
            if line.startswith('#EXTINF:-1'):
                segments, channel = line[:-1].split(',')
                group = re.findall(r'group-title="(.*?)"', segments)[0]
                if group != current_group:
                    if current_group != '':
                        self.new_lives.append('\n')
                    self.new_lives.append(group+',#genre#\n')
                    current_group = group
            else:
                self.new_lives.append(channel+','+line)
        return self


    def as_file(self, whether):
        if not whether:
            return False
        ext = '.txt' if self.type in ['.m3u','.m3u8'] else '.m3u'
        with open('./'+self.file_name+ext, 'w', encoding='UTF-8') as file:
            file.writelines(self.new_lives)

    def converto(self, as_file = False):
        if self.type == '.txt':
            self.txt_to_m3u()
        else:
            self.m3u_to_txt()
        self.as_file(as_file)

def json_to_txt(ipath: str):
    if not os.path.isfile(ipath) and not ipath.endswith('json'):
        raise TypeError("这不是一个JSON文件")
    with open(ipath, encoding='UTF-8') as json_file:
        json_data = json.load(json_file)
    opath = ipath.replace('.json', '.txt', -1)
    txt_file = open(opath, 'w', encoding='UTF-8')
    for grou in json_data:
        name = grou.get('name').strip()
        channels = grou.get('channel')
        txt_file.write(name+',#genre#\n')
        for channel in channels:
            ch_name = channel.get('name')
            for ch_url in channel.get('urls'):
                txt_file.write('{},{}\n'.format(ch_name,  ch_url))
        txt_file.write('\n')
    txt_file.close()

def txt_to_m3u(live: str):
    opath = live.replace('.txt', '.m3u', -1)
    m3u_file = open(opath, 'w', encoding='UTF-8')
    m3u_file.write('#EXTM3U\n')
    content = load_live(live)
    for group,channels in content.items():
        for channel, urls in channels.items():
            for url in urls:
                m3u_file.write('#EXTINF:-1 group-title="{}" tvg-logo="",{}\n'.format(group.replace(',#genre#\n', ''), channel))
                m3u_file.write(url)
    m3u_file.close()


def merge_live(live, another_live):
    pass

def load_live(live: str):
    data = {}
    channels = {}
    with open(live, encoding='UTF-8') as file:
        categorize = ""
        channel = ""
        url = ""
        for line in file.readlines():
            if line == "" or line == '\n': continue
            if line.endswith('#genre#\n'):
                if channels:
                    data.update({categorize: channels})
                categorize = line
                channels = {}
            else:
                channel, url = line.split(',')
                if channel not in channels:
                    channels[channel] = [url]
                else:
                    if url not in channels[channel]:
                        channels[channel].append(url)
    return data

def cn_live(channel:str):
    with open(channel,'r+',encoding='UTF-8') as json_file:
        json_data = json.load(json_file)
        cns = []
        for data in json_data:
            if data.get("country") == "CN":
                cns.append(data)
        json_file.seek(0)
        if cns:
            json.dump(cns, json_file, indent=4)
        json_file.truncate()
        

if __name__ == '__main__':
    parser = Parser('live.m3u')
    parser.m3u_to_txt().as_file(True)

    # string = 'group-title="🎣  NewTV" tvg-logo=""'
    # res = re.findall(r'group-title="(.*?)"', string)
    # print(res)