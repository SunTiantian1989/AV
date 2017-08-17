import json
import subprocess


class VideoInfo(object):
    def __init__(self,strFileName):
        str_cmd = r'ffprobe -v quiet -print_format json -show_format -show_streams -i ' + strFileName
        b = subprocess.check_output(str_cmd).decode('GB18030','ignore')
        info = json.loads(b)
        for stream in info['streams']:
            if stream['codec_type']=='video':
                self.codec_tag = stream['codec_tag_string']
                self.height = stream['coded_height']
                self.width = stream['coded_width']
        self.bit_rate = info['format']['bit_rate'][:-3]
        self.size = info['format']['size'][:-6]
