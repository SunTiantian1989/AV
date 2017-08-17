import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import gzip
import requests


def un_gzip(data):
    try:
        data = gzip.decompress(data)
    except:
        print("未经压缩，无需解压...")
    return data


class VideoInfo(object):
    def __init__(self, page_source):
        try:
            bsObj = BeautifulSoup(page_source, "html.parser")
            self.title = bsObj.find("div", {"id": "video_title"}).find("a").get_text()
            self.date = bsObj.find("div", {"id": "video_date"}).find("td", {"class": "text"}).get_text()
            self.length = bsObj.find("div", {"id": "video_length"}).find("span", {"class": "text"}).get_text()
            self.director = bsObj.find("div", {"id": "video_director"}).find("td", {"class": "text"}).get_text()
            self.maker = bsObj.find("div", {"id": "video_maker"}).find("td", {"class": "text"}).get_text()
            self.label = bsObj.find("div", {"id": "video_label"}).find("td", {"class": "text"}).get_text()
            point_with_kuohu = bsObj.find("div", {"id": "video_review"}).find("span", {"class": "score"}).get_text()
            if point_with_kuohu == '':
                self.review_point = 0
            else:
                self.review_point = int(float(point_with_kuohu[1:-1])*10)
            all_genres = bsObj.find("div", {"id": "video_genres"}).findAll("span", {"class": "genre"})
            self.genres_list=[]
            for genres in all_genres:
                self.genres_list.append(genres.find("a").get_text())
            all_cast=bsObj.find("div", {"id": "video_cast"}).findAll("span", {"class": "cast"})
            self.cast_list=[]
            for cast in all_cast:
                self.cast_list.append(cast.find("a").get_text())
            self.cover_remote_address = bsObj.find("div", {"id": "video_jacket"}).img.attrs["src"]
        except AttributeError as e:
            return None


def obtain_info_from_jav(video_number, is_cover_flag_exist, new_cover_name):
#    time.sleep(1)
    session = requests.session()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "}
    url = 'http://www.javlibrary.com/cn/vl_searchbyid.php?keyword='+video_number
    req = session.get(url, headers=headers)
    bsObj = BeautifulSoup(req.text, "html.parser")
    if "识别码搜寻结果" in bsObj.title.contents[0]:
        all_videos = bsObj.findAll("div", {"class": "video"})
        if len(all_videos) == 0:
            print(video_number+" 搜寻没有结果")
            return None
        for video in all_videos:
            if video.find("div", {"class": "id"}).get_text() == video_number:
                sub_url = video.a.attrs["href"]
                url = "http://www.javlibrary.com/cn/"+sub_url
                req = session.get(url, headers=headers)
                break
            print(video_number + " 搜寻没有结果")
            return None
    print(video_number,' GET!')
    video_info = VideoInfo(req.text)
    if not is_cover_flag_exist:
        # 下载图片
        img_file = urlopen(video_info.cover_remote_address)
        byte = img_file.read()
        write_file = open(new_cover_name, 'wb')
        write_file.write(byte)
        write_file.close()
    return video_info
