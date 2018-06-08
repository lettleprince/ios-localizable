#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Tony'
__date__ = '2018/06/08 12:06'

import sys
import os
import re

# 只针对字符串本地化和图片本地，其他暂未考虑

# 需要搜索的项目所在目录
ProjectDir = '../Localizable/Classes'
# 本地化资源文件所在目录，相对于脚本所在目录
LocalizableDir = '../Localizable/Resources'
# 图片本地换资源文件名称
ImageLocalizableFileName = 'ImageLocalizable'
# 字符串本地换资源文件名称
LanguageLocalizableFileName = 'Language'

LocalizableDefine = 'LocalizedString'
ImageLocalizableDefine = 'LocalizedImage'

# 将系统当前目录设置为项目根目录
# os.path.abspath(__file__)为当前文件所在绝对路径
# os.path.dirname为文件所在目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 获取目录下所有文件
def get_all_file_path(dir_name):
    result = []
    for root, dirs, files in os.walk(dir_name):
        for filename in files:
            # print(os.path.join(root, filename))
            file_path = os.path.join(root, filename)
            result.append(file_path)
    return result

# 获取所有类文件
def get_all_class_file_path():
    result = []
    for file_path in get_all_file_path(ProjectDir):
        #  扩展名过滤
        ext_names = ['h', 'm', 'mm']
        if os.path.splitext(file_path)[1][1:] in ext_names:
            result.append(file_path)
    return result

# 获取所有本地化资源文件
def get_all_localizable_file_path(file_base_name):
    result = []
    for file_path in get_all_file_path(LocalizableDir):
        filename = os.path.basename(file_path)
        #  文件名过滤
        if os.path.splitext(filename)[0] == file_base_name:
            result.append(file_path)
    return result

# 通过宏获取所有需要本地化的键
def get_all_localizable_key(localizable_define):
    keys = []
    rex = localizable_define + '\(@"([^"]*)"\)'
    pattern = re.compile(rex, re.DOTALL)
    for path in get_all_class_file_path():
        with open(path, 'r') as f:
            content = f.read()
            for result in pattern.finditer(content):
                keys.append(result.group(1))
    return keys

CommentTextFormat = '''/* 
  %s
  自动生成的本地化资源
*/

'''

# 向所有的本地化资源中写入键值
def write_to_localizable_file(keys, paths):
    for file_path in paths:
        with open(file_path, 'w') as f:
            comment_text = CommentTextFormat % os.path.basename(file_path)
            f.write(comment_text)
            for key in keys:
                content = '"' + key + '"="' + key + '"'
                print(content)
                f.write(content)

def main():
    keys = get_all_localizable_key(LocalizableDefine)
    language_localizable_file_paths = get_all_localizable_file_path(LanguageLocalizableFileName)
    write_to_localizable_file(keys, language_localizable_file_paths)

    keys = get_all_localizable_key(ImageLocalizableDefine)
    image_localizable_file_paths = get_all_localizable_file_path(ImageLocalizableFileName)
    write_to_localizable_file(keys, image_localizable_file_paths)

if __name__ == '__main__':
    main()