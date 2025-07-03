import os
import re
import requests
from bs4 import BeautifulSoup

def get_playlist_name(playlist_url):
    header = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)"}
    response = requests.get(playlist_url, headers=header)
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return None

    #print(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')

    playlist_name = soup.select('.f-ff2.f-brk')[0].get_text()
    if playlist_name:
        return playlist_name
    else:
        print("Playlist name not found")
        return None

def output_path(out_path_list, id):
    out_path = get_playlist_name("https://music.163.com/playlist?id=" + id) + ".m3u8"
    with open(out_path, 'w', encoding='utf-8') as file:
        for path in out_path_list:
            file.write(path + '\n')
    return

def convert_format(input_str_list, id):
    music_path = input("输入音乐所在目录:\n").strip().strip("'")
    print(music_path)
    new_path_list = []
    for line in input_str_list:
        cleaned_str = re.sub(r'\d{8,10} - ', '', line).strip()
        new_path = f"{music_path}/{cleaned_str}.mp3"
        new_path_list.append(new_path)
    #返回新路径列表，歌单id
    return new_path_list, id

def origin_path():
    in_file = input("请输入原始文件路径: \n").strip().strip("'")
    parts = in_file.split("_")
    with open(in_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    #返回文件中每行字符组成的列表与文件名中间的歌单id
    return lines, parts[2]

def main():
    output_path(*convert_format(*origin_path()))

if __name__ == "__main__":
    main()
