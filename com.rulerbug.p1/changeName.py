import os

# 目标文件夹
dirPath = r"C:\Users\Administrator\Desktop\金丝猴租赁_slices"
# 需要改文件名的信息，比如    "矩形(1).png"改为 "home_pre.png"
nameMap = {

    "btu_mrdz.png": "btu_mrdz12312.png",






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
