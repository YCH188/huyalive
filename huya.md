## 此程序在Ubuntu系统下测试无误
需要安装requests、json、re等Python模块
安装录屏软件模块
sudo apt-get install ffmpeg
## 如果在Windows系统下使用，需修改程序语句，并将ffmpeg.exe放在当前路径下
os.system('{}/ffmpeg.exe -i {} -c copy {}'.format(os.getcwd()……