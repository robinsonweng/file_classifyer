import yaml
import os
import sys
import shutil
import colorama
import argparse
from os import listdir
from os.path import isfile
from colorama import Fore


VERSION = 'File classifyer 1.0'
OS = ''

colorama.init(autoreset=True)

class FileClassify(object):
    def __init__(self):
        # read config
        with open('..\\settings\\path.yaml', 'r', encoding='utf-8') as f:
            self.path = yaml.load(f.read(), Loader=yaml.BaseLoader)
        with open('..\\settings\\rule.yaml', 'r', encoding='utf-8') as f:
            self.rule = yaml.load(f.read(), Loader=yaml.BaseLoader)
    
        self.description = 'Organize and classify the file'
        self.parse = argparse.ArgumentParser(description=self.description)

        self.parse.add_argument('-v', '--version', action="store_true")

        self.arg = self.parse.parse_args()

    def dir_check(self):
        """
        check if path exist, if not return warning
        """
        brk = False
        print(Fore.GREEN + '\nChecking dir...')
        for row in self.path:
            path = self.path[row]
            if os.path.exists(path):
                print(f'{row} dir({path}):', Fore.GREEN + 'exist')
            else:
                # shoud exit the script
                print(f"{row} dir({path}):", Fore.RED + " don't exist")
                brk = True
        if brk:
            print(Fore.RED + 'Dir missing, please check the path.yaml')
            exit()
    
    def scan_file(self):
        """
        caculate the amount of the file category
        """
        active_path = self.path['activefolder']
        # file only
        allfiles = [ f for f in listdir(active_path)\
                     if isfile(os.path.join(active_path, f))]

        # music document picture video
        self.amount = [
            ["music"],
            ["document"],
            ["picture"],
            ["video"]
        ]
        self.other = []
        for files in allfiles:
            for index, r in enumerate(self.rule.items()):
                for ex in r[1]:
                    if files.endswith(ex):
                        cate_path = self.path[self.amount[index][0]]
                        path = os.path.join(cate_path, files)
                        self.amount[index].append(path)
                        break
                else:
                    continue
                break
            else:
                self.other.append(files)

        print(Fore.GREEN + '\nResult:')
        for a in self.amount:
            print(f'{a[0]}: {len(a)-1} files')

    def show_tree(self):
        print(Fore.GREEN + '\nThese files will be classify as:\n')
        for path_list in self.amount:
            file_str = ''
            dir_str = ''
            for path in path_list[1:]:
                # print(path)    
                root = os.path.dirname(path)
                filename = os.path.basename(path)
                dir_str = '    |' + '-' * 4 + root
                file_str += '    |' * 2 + '-' * 4 + filename + '\n'
            print(Fore.GREEN + dir_str)
            print(file_str, end='')
        
        print(Fore.YELLOW + "These files didn't move:")
        for o in self.other:
            other = os.path.basename(o)
            file_str += '    |' * 2 + '-' * 4 + other + '\n'
        print(file_str, end='')

    def put_in_bucket(self):
        """
        put the file in the right dir
        """
        print(Fore.YELLOW + 'Warning!', end='')
        print(' This will cover the same files.')
        print('Are you sure?(Y\\N)')

        for path_list in self.amount:
            for path in path_list[1:]:
                filename = os.path.basename(path)
                prev = self.path['activefolder']+ '\\' + filename
                shutil.move(prev, path)

    def run(self):
        pass

if __name__ == "__main__":
    fileclassify = FileClassify()
    fileclassify.dir_check()
    fileclassify.scan_file()
    fileclassify.show_tree()
    # fileclassify.put_in_bucket()