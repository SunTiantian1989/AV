import initial_database
import sqlite3
import os
import re
import obtain_info_from_avso_by_requests as avso
from obtain_video_info import VideoInfo
if not os.path.isfile('AV.db'):
    initial_database.initial_database()
video_dir = r'E:\5娱乐相关\材料力学\视频\无码'
if not os.path.exists(video_dir):
    print('目录不存在！')
else:
    conn = sqlite3.connect('AV.db')
    # 列出目录下的所有文件和目录
    dir_obj_list = os.listdir(video_dir)
    for obj_name in dir_obj_list:
        obj_full_path = os.path.join(video_dir, obj_name)
        if not os.path.isdir(obj_full_path):
            # 假设目录下全部为视频文件与图片文件，暂时不判断其他ext
            file_name, ext_name = os.path.splitext(obj_name)
            if (ext_name == '.avi')or(ext_name == '.mkv')or(ext_name == '.mp4')or(ext_name == '.rmvb')or(ext_name == '.wmv'):
                video_number = file_name
                new_video_name = os.path.join(video_dir, video_number + ext_name)
                new_cover_name = os.path.join(video_dir, video_number + '.jpg')
                # 数据库里没有就加记录
                if not os.path.exists(new_cover_name):
                    video_info = avso.obtain_info_from_jav(video_number, False, new_cover_name)
                    if video_info is None:
                        continue
    for obj_name in dir_obj_list:
        obj_full_path = os.path.join(video_dir, obj_name)
        if not os.path.isdir(obj_full_path):
            # 假设目录下全部为视频文件与图片文件，暂时不判断其他ext
            file_name, ext_name = os.path.splitext(obj_name)
            if (ext_name == '.avi')or(ext_name == '.mkv')or(ext_name == '.mp4')or(ext_name == '.rmvb')or(ext_name == '.wmv'):
                video_number = file_name
                new_video_name = os.path.join(video_dir, video_number + ext_name)
                new_cover_name = os.path.join(video_dir, video_number + '.jpg')
                # 数据库里没有就加记录
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM videos WHERE number=?', (video_number, ))
                if len(cursor.fetchall()) != 0:
                    continue
                if os.path.exists(new_cover_name):
                    video_info = avso.obtain_info_from_jav(video_number, True, new_cover_name)
                else:
                    video_info = avso.obtain_info_from_jav(video_number, False, new_cover_name)
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
