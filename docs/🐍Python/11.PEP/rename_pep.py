#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2020/8/15 19:18
"""
将原库加上hexo头，同时修改文件名称（点和空格用中划线替换）
"""
import pathlib


def get_file(file_path):
    """
    获取给定目录下的所有文件的绝对路径
    :param file_path: 文件目录
    :param pattern: 默认返回所有文件，也可以自定义返回文件类型，例如：pattern="*.py"
    :return: 文件路径列表
    """
    all_file = []
    files = pathlib.Path(file_path)
    f = files.rglob('*.md')
    for file in f:
        pure_path = pathlib.PurePath(str(file))
        dirname = pure_path.parent
        name = pure_path.name
        if '-' in name and not name.startswith('pep'):
            new_name = f"{dirname}/pep-{name.split('-')[0].zfill(4)}.md"
            print(new_name)
            target = pathlib.Path(new_name)
            p = pathlib.Path(file)
            p.rename(target)
            # p = pure_path.with_name(new_name)
            # print(p)
            # break
    # return list(files)
        all_file.append(file)
    return all_file


# def split_name(fn='10.1 斐波那契数列.md'):
#     """
#     [Split a string only by first space in python - StackOverflow](https://stackoverflow.com/questions/30636248/split-a-string-only-by-first-space-in-python)
#     return : 10-1-斐波那契数列.md
#     """
#     a, b = fn.split('.', 1)
#     c, d = b.split(' ', 1)
#     return '-'.join([a, c, d])
#
#
# def write_to_md():
#     """
#     1. 找文件
#     2. 加头
#     3. 重写文件
#     :return:
#     """
#     f_list = get_file('.', pattern="*.md")
#     for file in f_list:
#         has_num = str(file).count('.') == 2
#
#         title = pathlib.PurePath(str(file)).stem
#         print(title, file, '-------------')
#         path = pathlib.Path(file)
#         with open(path, encoding='utf-8') as f:
#             old = f.readlines()
#             head = [
#                 '---\n',
#                 f'title: {title}\n',
#                 'toc: true  \n',
#                 'date: 2019-08-07 12:27:56 \n',
#                 'tags: [面试, 技术]\n',
#                 '---\n'
#             ]
#
#             head.extend(old[1:])
#
#         path.unlink()  # 删除原来文件
#
#         new_fn = split_name(str(file)) if has_num else str(file)
#
#         with open(new_fn, 'w', encoding='utf-8') as f:
#             f.writelines(head)
#     return 0


if __name__ == '__main__':
    path = pathlib.Path('./')
    a = get_file(path)
    print(a)
