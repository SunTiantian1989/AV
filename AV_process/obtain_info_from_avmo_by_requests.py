import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re


def search_results_process(search_results,video_number):
    if len(search_results) == 0:
        return None
    elif len(search_results) == 1:
        result = search_results[0]
        if result.find("date").get_text() == video_number:
            video_url = result.attrs["href"]
            return video_url
        else:
            return None
    else:
        for result in search_results:
            if result.find("date").get_text() == video_number:
                video_url = result.attrs["href"]
                return video_url
        return None



class VideoInfo(object):
    def __init__(self, page_source):
        try:
            bsObj = BeautifulSoup(page_source, "html.parser")
            self.title = bsObj.find("h3").get_text()
            temp_text= bsObj.find(text='发行时间:').parent.parent.get_text()
            pattern_date = r'(\d{4}-\d{2}-\d{2})'
            try:
                m = re.search(pattern_date, temp_text)
            except Exception as e:
                print('正则化失败！')
            self.date = m.group(1)
            temp_text = bsObj.find(text='长度:').parent.parent.get_text()
            pattern_length = r'(\d{2,3})'
            try:
                m = re.search(pattern_length, temp_text)
            except Exception as e:
                print('正则化失败！')
            self.length = m.group(1)
            temp_obj=bsObj.find(text='导演:')
            if temp_obj is None:
                self.director = '---'
            else:
                self.director = bsObj.find(text='导演:').parent.parent.find("a").get_text()
            self.maker = bsObj.find(text='制作商: ').parent.next_sibling.next_sibling.find("a").get_text()
            if bsObj.find(text='发行商: ') is None:
                self.label = '---'
            else:
                self.label = bsObj.find(text='发行商: ').parent.next_sibling.next_sibling.find("a").get_text()

            temp_series = bsObj.find(text='系列:')
            if temp_series is None:
                self.series = '---'
            else:
                self.series = temp_series.parent.next_sibling.next_sibling.find("a").get_text()
            self.review_point = 0
            all_genres = bsObj.find(text='类别:').parent.next_sibling.next_sibling.findAll("span", {"class": "genre"})
            self.genres_list=[]
            for genres in all_genres:
                self.genres_list.append(genres.find("a").get_text())
            if bsObj.find("div", {"id": "avatar-waterfall"}) is None:
                self.cast_list = []
            else:
                all_cast=bsObj.find("div", {"id": "avatar-waterfall"}).findAll("span")
                self.cast_list=[]
                for cast in all_cast:
                    self.cast_list.append(cast.get_text())
            self.cover_remote_address = bsObj.find("img").attrs["src"]
        except AttributeError as e:
            return None


def obtain_info_from_jav(video_number, is_cover_flag_exist, new_cover_name):
#   time.sleep(3)
    session = requests.session()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "}
    # url = 'https://avmo.pw/cn/search/' + video_number https://avio.pw/cn
    url = 'https://avio.pw/cn/search/' + video_number
    req = session.get(url, headers=headers)
    bsObj = BeautifulSoup(req.text, "html.parser")
    search_results = bsObj.find("div", {"id": "waterfall"}).findAll("a", {"class": "movie-box"})
    url = search_results_process(search_results, video_number)
    if url is None:
        print(video_number + " 搜寻没有结果")
        return None
    else:
        print(video_number, ' GET!')
        req = session.get(url, headers=headers)
        video_info = VideoInfo(req.text)
        if not is_cover_flag_exist:
            # 下载图片
            img_content = session.get(video_info.cover_remote_address, headers=headers)
            with open(new_cover_name, 'wb') as f:
                f.write(img_content.content)
        return video_info
