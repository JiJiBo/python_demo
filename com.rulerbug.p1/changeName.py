import os

# 目标文件夹
dirPath = r"D:\360安全浏览器下载\画板_slices"
# 需要改文件名的信息，比如    "矩形(1).png"改为 "home_pre.png"
nameMap = {
    "矩形(1).png": "home_pre.png",
    "矩形.png": "home_def.png",
    "矩形备份 2(1).png": "my_pre.png",
    "矩形备份 2.png": "my_def.png",
    "矩形备份(1).png": "analyze_pre.png",
    "analyze_def2.png": "analyze_def.png"
}


def get_file_path(root_path):
    # 获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        # 获取目录或者文件的路径
        dir_file_path = os.path.join(root_path, dir_file)
        filename = os.path.basename(dir_file_path)
        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            # 递归获取所有文件和目录的路径
            get_file_path(dir_file_path)
        else:
            if filename in nameMap.keys():
                os.rename(dir_file_path, root_path + "\\" + nameMap[filename])


if __name__ == "__main__":
    # 根目录路径
    root_path = dirPath
    get_file_path(root_path)
