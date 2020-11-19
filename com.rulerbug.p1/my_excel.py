from mutagen.mp3 import MP3, HeaderNotFoundError
import os
import re
import requests
# from pydub import AudioSegment
from requests_toolbelt import MultipartEncoder

from shutil import copyfile

dirPath = r"F:\music\MP3"
wavPath = r"F:\music\wav"
picturePath = r"F:\music\歌手图片"
otherPicker = r"F:\music\歌手图片\其他.jpg"
pickers = {}
# excelPath = r"C:\Users\Administrator\Music\音乐上传管理数据导入模板.xlsx"
reg = "(^.+)\s-{1}\s(.+).mp3$"
postUrl = "http://47.95.11.42:9090/music/uploadingMusic"

error_header = "a error  解析失败"


class GetMp3Info():
    '''获取歌曲信息'''

    def __init__(self, path, filename):
        songFile = MP3(path)
        self.filename = filename
        self.path = path
        self.getTitle(filename)
        self.getArtist(filename)
        self.getAlbum(filename)
        self.isCanParseMothod(filename)
        self.getLength(songFile)
        self.picker = ""
        try:
            self.picker = pickers[self.Album]
        except(KeyError):
            self.picker = pickers["其他"]
            # copyfile(otherPicker,r"F:\music\歌手图片\\"+self.Album+".jpg")

    def getTitle(self, filename):
        if re.match(reg, filename) == None:
            self.Title = "null"
            return
        self.Title = re.match(reg, filename).group(1)

    def getArtist(self, filename):
        if re.match(reg, filename) == None:
            self.Artist = "null"
            return
        self.Artist = re.match(reg, filename).group(2)

    def getAlbum(self, filename):
        if re.match(reg, filename) == None:
            self.Album = "null"
            return
        self.Album = re.match(reg, filename).group(1)

    def getLength(self, songFile):
        '''获取文件播放时时长'''
        timeLength = int(songFile.info.length)
        mintime = timeLength // 60  # 转换为分钟
        sectime = timeLength % 60  # 剩余的转换为秒
        if sectime < 10:
            sectime = '0' + str(sectime)
        else:
            sectime = str(sectime)
        self.length = str(mintime) + ":" + sectime

    def isCanParseMothod(self, filename):
        self.isCanParse = re.match(reg, filename) != None


def get_file_path(root_path):
    # 获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    count = 1
    for dir_file in dir_or_files:
        # 获取目录或者文件的路径
        dir_file_path = os.path.join(root_path, dir_file)
        filename = os.path.basename(dir_file_path)

        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            # 递归获取所有文件和目录的路径
            get_file_path(dir_file_path)
        else:
            try:
                song = GetMp3Info(dir_file_path, filename)
            except (HeaderNotFoundError):
                print("解析失败", filename)
                if error_header not in filename:
                    print("解析失败  重命名")
                    os.rename(dir_file_path, root_path + "\\" + error_header + " code  1 " + filename)
                    continue
            if " - " in song.Album:
                print("解析失败", filename)
                if error_header not in filename:
                    print("解析失败  重命名")
                    os.rename(dir_file_path, root_path + "\\" + error_header + "  code  2 " + filename)
                    continue
            if song.isCanParse:
                # print("-" * 20)
                # print("数量：", count)
                count += 1
                # print("\n\t", "title：", song.Title, "\n\t", "歌曲名：", song.Artist, "\n\t", "作者：", song.Album, "\n\t",
                #       "图片：", song.picker, "\n\t",
                #       song.length, "\n\t",
                #       song.isCanParse)
                # os.remove(dir_file)
                # sound = AudioSegment.from_mp3(dir_file_path)
                # sound.export(dirPath + filename, format='wav')


# def writeToExcel(song):
#     data = openpyxl.load_workbook(excelPath)
#     table = data["Export"]
#     table = data.active
#     nrows = table.max_row
#     ncolumns = table.max_column
#     values = ['0', '', song.length, '2020-10-10 17:11:00', song.artist, song.title, song.album, "", song.path, "", "",
#               ""]
#     row = 1
#     for value in values:
#         table.cell(nrows + 1, row).value = value
#         row = row + 1
#     data.save(excelPath)

def postFile(song):
    m = MultipartEncoder({
        'files': (song.filename, open(song.path, 'rb'), 'audio/mpeg')
    })
    headers = {
        "satoken": "be441ef7-1ec3-40d0-8a65-35834dfe3b1e",
        "Content-Type": m.content_type
    }
    res = requests.post(postUrl, data=m, headers=headers).json()
    print(res)


# def postFile(song):
#     f = open(song.path, 'rb')
#     file = {
#         "file": (song.filename, f.read()),  # 引号的file是接口的字段，后面的是文件的名称、文件的内容
#         "satoken": "be441ef7-1ec3-40d0-8a65-35834dfe3b1e",  # 如果接口中有其他字段也可以加上
#     }
#     encode_data = encode_multipart_formdata(file)
#     file_data = encode_data[0]
#     headers_from_data = {
#         "Content-Type": encode_data[1],
#         "satoken": "be441ef7-1ec3-40d0-8a65-35834dfe3b1e"
#     }
#     response = requests.post(url=postUrl, headers=headers_from_data, data=file_data).json()
#     print("成功上传", song.Title, response)


def loadPickers(picturePath):
    dir_or_files = os.listdir(picturePath)
    for dir_file in dir_or_files:
        dir_file_path = os.path.join(root_path, dir_file)
        filename = os.path.basename(dir_file_path)[0:-4]
        pickers[filename.lower()] = dir_file_path


if __name__ == '__main__':
    root_path = dirPath
    loadPickers(picturePath)
    # print(pickers)
    get_file_path(root_path)
