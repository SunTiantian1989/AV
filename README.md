# AV_process
## 主要功能描述
用于整理硬盘上大量的日本AV，包括无码和有码，并通过网页显示结果。
- 自动从网上抓取相关信息与封面图片
- 整理并存入数据库
- 使用flask展示结果

## 前置条件
- 目前在Windows7 x64系统下开发，python版本3.5.2（3.6下某些库有问题）
- 能够连接[https://avio.pw/cn](https://avio.pw/cn "avio.pw/cn")、[https://avso.pw/cn/](https://avso.pw/cn/ "avso.pw/cn/")、[http://www.javlibrary.com/cn/](http://www.javlibrary.com/cn/ "www.javlibrary.com/cn/")，请自备梯子。
- 获取视频信息需要安装ffmpeg，好像是拷贝几个动态库到system32，请自行Google
- 需要一些python库，目前开发使用的IDE是JetBrains PyCharm Community Edition 2016.3.1，缺什么就装什么吧。

## 使用方法
1. 运行AV_process\initial_database.py，创建AV数据库
2. 分别替代AV_process\main_wuma与AV_process\main_youma中video_dir的路径，上网下载AV的信息并存入数据库（**注意：目录中不能有空格**）
3. 拷贝AV.db至flask文件夹，将有码无码文件夹中的图片拷贝至flask\static\jpg
4. 运行START.bat