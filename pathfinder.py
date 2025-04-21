import os
import fnmatch

def if_exe(directory,file):
    ls = file.split(directory)
    # print(ls)
    if('\\' not in ls[1]):
        return True
    

def list_exe_files(directory):
    exe_files = []
    for root, dirs, files in os.walk(directory):
        for file in fnmatch.filter(files, '*.exe'):
            exe_files.append(os.path.join(root, file))
    return exe_files

directory = 'C:\\Users\\BarnwalA\\AppData\\Local\\Microsoft\\WindowsApps\\' # Change this to the directory you want to search
exe_files = list_exe_files(directory)
main_exe_files = []
for file in exe_files:
    if(if_exe(directory,file)):
        main_exe_files.append(file)
for exe_file in main_exe_files:
    print(exe_file)