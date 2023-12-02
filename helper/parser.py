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
        if not os.path.isfile(os.path.join(os.path.dirname(__file__), file)) or self.type not in ['.txt','.m3u','.m3u8']:
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
            print(line.split(','))
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

if __name__ == '__main__':
    parser = Parser('list.txt')
    parser.txt_to_m3u().as_file(True)

    # string = 'group-title="🎣  NewTV" tvg-logo=""'
    # res = re.findall(r'group-title="(.*?)"', string)
    # print(res)