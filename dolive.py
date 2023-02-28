#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

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
    cn_live('channels.json')