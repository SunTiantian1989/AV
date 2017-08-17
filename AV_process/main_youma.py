import initial_database
import sqlite3
import os
import re
import obtain_info_from_avmo_by_requests as avmo
import obtain_info_from_jav_by_requests as jav
from obtain_video_info import VideoInfo
if not os.path.isfile('AV.db'):
    initial_database.initial_database()
video_dir = r'E:\5娱乐相关\材料力学\视频\有码'
if not os.path.exists(video_dir):
    print('目录不存在！')
else:
    conn = sqlite3.connect('AV.db')
    # 列出目录下的所有文件和目录
    dir_obj_list = os.listdir(video_dir)
    # 第一遍处理图片
    for obj_name in dir_obj_list:
        obj_full_path = os.path.join(video_dir, obj_name)
        if not os.path.isdir(obj_full_path):
            # 假设目录下全部为视频文件与图片文件，暂时不判断其他ext
            file_name, ext_name = os.path.splitext(obj_name)
            if ext_name == '.jpg':
                pattern = r'([A-Za-z]{2,5})[ -_]?(\d{2,5})'
                try:
                    m = re.search(pattern, file_name)
                except Exception as e:
                    print('正则化失败！')
                    continue
                if m is None:
                    pass
                video_number = m.group(1).upper() + '-' + m.group(2)
                cover_name = os.path.join(video_dir, file_name + '.jpg')
                new_cover_name = os.path.join(video_dir, video_number + '.jpg')
                if not os.path.exists(new_cover_name):
                    os.rename(cover_name, new_cover_name)
    for obj_name in dir_obj_list:
        obj_full_path = os.path.join(video_dir, obj_name)
        if not os.path.isdir(obj_full_path):
            # 假设目录下全部为视频文件与图片文件，暂时不判断其他ext
            file_name, ext_name = os.path.splitext(obj_name)
            if (ext_name == '.avi')or(ext_name == '.mkv')or(ext_name == '.mp4')or(ext_name == '.rmvb')or(ext_name == '.wmv'):
                pattern = r'([A-Za-z]{2,5})[ -_]?(\d{2,5}) ?([ABab]?)'
                try:
                    m = re.search(pattern, file_name)
                except Exception as e:
                    print('正则化失败！')
                    continue
                video_number = m.group(1).upper()+'-'+m.group(2)
                # 视频重命名
                video_name = m.group(1).upper() + '-' + m.group(2) + '' + m.group(3)
                new_video_name = os.path.join(video_dir, video_name + ext_name)
                if not os.path.exists(new_video_name):
                    os.rename(obj_full_path, new_video_name)
                # 没有图片就下载图片
                new_cover_name = os.path.join(video_dir, video_number + '.jpg')
                # if not os.path.exists(new_cover_name):
                #     video_info = jav.obtain_info_from_jav(video_number, True, new_cover_name)
                #     if video_info is None:
                #         print('JAV Fail, try AVMO')
                #         video_info = avmo.obtain_info_from_jav(video_number, True, new_cover_name)
                #         if video_info is None:
                #             continue
                # 数据库里没有就加记录
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM videos WHERE number=?', (video_number, ))
                if len(cursor.fetchall()) != 0:
                    continue
                if os.path.exists(new_cover_name):
                    video_info = jav.obtain_info_from_jav(video_number, True, new_cover_name)

                    if video_info is None:
                        print('JAV Fail, try AVMO')
                        video_info = avmo.obtain_info_from_jav(video_number, True, new_cover_name)
                else:
                    # video_info = jav.obtain_info_from_jav(video_number, False, new_cover_name)
                    video_info = None
                    if video_info is None:
                        print('JAV Fail, try AVMO')
                        video_info = avmo.obtain_info_from_jav(video_number, False, new_cover_name)
                if video_info is None:
                    continue
                cursor.execute('SELECT * FROM videos WHERE number=? AND date=?', (video_number, video_info.date))
                if len(cursor.fetchall()) == 0:
                    video_stream_info = VideoInfo(new_video_name)
                    cursor.execute('''INSERT INTO videos (number,title,date,length,
                    director,maker,label,review_point,codec_tag,height,width,bit_rate,size) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                                   (video_number,
                                    video_info.title,
                                    video_info.date,
                                    video_info.length,
                                    video_info.director,
                                    video_info.maker,
                                    video_info.label,
                                    video_info.review_point,
                                    video_stream_info.codec_tag,
                                    video_stream_info.height,
                                    video_stream_info.width,
                                    video_stream_info.bit_rate,
                                    video_stream_info.size))

                for genre in video_info.genres_list:
                    cursor.execute('SELECT * FROM genres WHERE genre_name=?', (genre,))
                    if len(cursor.fetchall()) == 0:
                        cursor.execute('INSERT INTO genres (genre_name) VALUES (?)', (genre,))
                    cursor.execute('SELECT * FROM genres_in_videos WHERE video_number=? AND genre_name=?', (video_number, genre))
                    if len(cursor.fetchall()) == 0:
                        cursor.execute('INSERT INTO genres_in_videos (video_number, genre_name) VALUES (?,?)', (video_number, genre))
                for cast in video_info.cast_list:
                    cursor.execute('SELECT * FROM casts WHERE cast_name=?', (cast,))
                    if len(cursor.fetchall()) == 0:
                        cursor.execute('INSERT INTO casts (cast_name) VALUES (?)', (cast,))
                    cursor.execute('SELECT * FROM casts_in_videos WHERE video_number=? AND cast_name=?', (video_number, cast))
                    if len(cursor.fetchall()) == 0:
                        cursor.execute('INSERT INTO casts_in_videos (video_number, cast_name) VALUES (?,?)', (video_number, cast))
                cursor.close()
                conn.commit()
    conn.close()
