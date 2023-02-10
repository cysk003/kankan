import json

with open('live.json', encoding='UTF-8') as json_file:
    json_data = json.load(json_file)

txt_file = open('live.txt', 'w', encoding='UTF-8')

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