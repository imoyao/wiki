#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2020/12/12 20:48
"""
该脚本会递归替换执行目录下的文件名称
在要批处理的目录的上级运行该脚本
1. 如果没有给定ROOT_PATH，则直接以脚本所在目录为root
2. 否则，以用户给定为准
3. 我们可以给定rename的多个根目录，也可以直接以root为根目录，取决于你的“一级目录”是否很多
"""

import os
import pathlib
import re

current_path = os.path.dirname(os.path.abspath(__file__))
# 需要处理目录的绝对路径
ROOT_PATH = os.path.join(current_path, 'docs')
EXCLUDE_DIR = ['.vuepress', '@pages', '_posts', 'styles', 'images']

START_REMOVE_LISTS = ['.', '-', '_']


def get_exclude_children(exclude_dir):
    """
    获取被排除目录的子目录并添加到子目录中
    :param exclude_dir: str,文件路径名称
    :return: set,文件路径名称
    """
    origin_dir = exclude_dir[:]
    file_list = []
    for _dir in exclude_dir:
        exclude_dir_children = os.path.join(ROOT_PATH, _dir)

        for root, dirs, files in os.walk(exclude_dir_children):
            origin_dir.extend(dirs)
            file_list.extend(files)
    return set(origin_dir), set(file_list)


def reg_startswith(check_str, reg):
    """
    10.foo.md  >>> re.match.obj
    bar  >>> None
    :param check_str:str,被检查字符
    :param reg:str,正则表达式
    :return:匹配对象或None对象或None
    """
    return re.match(fr'^{reg}', check_str)


def is_md_file(file_path):
    """
    指定文件是md文件
    :param file_path:
    :return:
    """
    return pathlib.PurePath(file_path).suffix[1:].lower() == 'md'


def full_path(_root, file):
    return pathlib.PurePath(_root).joinpath(file)


def order_file_list_by_ctime(root, file_lists):
    """
    文件以创建时间排序
    :param root:
    :param file_lists:
    :return:
    """
    file_lists.sort(key=lambda file: pathlib.Path(full_path(root, file)).stat().st_ctime)

    filter_path = []
    for path in file_lists:
        f_path = full_path(root, path)
        if pathlib.Path(f_path).is_file():
            if is_md_file(f_path):
                filter_path.append(path)

    return filter_path


def make_rename(sub_line):
    """
    _xx.yyy:xx-yyy
    xx-yyy:xx-yyy
    xx.yyy:xx-yyy
    -xx.yyy:xx-yyy
    .xx-yyy:xx-yyy
    你好:你好
    💻:💻
    :param sub_line:
    :return:
    """
    # 如果开头的数字和后面的名称中间包含下方字符，则做截取操作
    if sub_line and sub_line[0] in START_REMOVE_LISTS:
        slice_symbol_str = sub_line[1:]
    else:
        slice_symbol_str = sub_line

    if '.' in slice_symbol_str:
        str_replace_dot_inline = slice_symbol_str.replace('.', '-')
        rename_str = str_replace_dot_inline
    else:
        rename_str = slice_symbol_str

    return rename_str


def rename_path_without_exclude(root_path, exclude_seq):
    """
    获取指定目录下排除默写目录的子目录
    :param root_path: str,
    :param exclude_seq: iterable,
    :return:
    """
    exclude_dirs, exclude_files = exclude_seq

    # def _not_in(all_seq, filter_seq):
    #     """
    #     使用 not in
    #     :param all_seq:
    #     :param filter_seq:
    #     :return:
    #     """
    #     return [item for item in all_seq if item not in filter_seq]

    # def _filter_sth(seq, exclude):
    #     """
    #     使用filter
    #     :param seq:
    #     :param exclude:
    #     :return:
    #     """
    #     return list(filter(lambda x: x not in exclude, seq))

    def _subtract_set(seq, exclude):
        """
        差集法
        :param seq:
        :param exclude:
        :return:
        """
        return list(set(seq) - set(exclude))

    for root, dirs, files in os.walk(root_path, topdown=False):
        # [python - Excluding directories in os.walk - Stack Overflow]
        # (https://stackoverflow.com/questions/19859840/excluding-directories-in-os-walk)
        # 此处有三种去重的方式，选择~~自己习惯的~~，性能最好且见名识意的
        dirs[:] = _subtract_set(dirs, exclude_dirs)
        files[:] = _subtract_set(files, exclude_files)

        count_set = set()
        count = 0

        def handler_action(_root, path_item, is_file=True):
            nonlocal count, count_set
            add_suffix = ''
            if is_file:
                add_suffix = '.md'

            reg_exp = r'\d+'
            reg_match_obj = reg_startswith(path_item, reg_exp)
            if reg_match_obj:
                # 本来有数字
                digital = reg_match_obj.group()
                count = int(digital)
                count_set.add(count)
                if is_file:
                    deal_line = pathlib.PurePath(path_item).stem
                else:
                    deal_line = pathlib.PurePath(path_item).parts[-1]

                sub_line = re.sub(reg_exp, "", deal_line)

                if sub_line.startswith('.'):
                    sub_line = sub_line[1:]
                sub_name = make_rename(sub_line)
                new_name_with_suffix = f'{digital}.{sub_name}{add_suffix}'

            else:
                if is_file:
                    path_str = pathlib.PurePath(path_item).stem
                else:
                    path_str = pathlib.PurePath(path_item).parts[-1]

                new_name = make_rename(path_str)
                # 找出最大count，然后+1作为新编号
                if count_set:
                    count = max(count_set)
                count += 1
                count_set.add(count)

                new_name_with_suffix = f'{count:02}.{new_name}{add_suffix}'

            old = os.path.join(_root, path_item)
            new = os.path.join(_root, new_name_with_suffix)
            return old, new

        for dir_item in dirs:
            old_dir_with_full_path, new_dir_with_full_path = handler_action(root, dir_item, is_file=False)
            rename_path(old_dir_with_full_path, new_dir_with_full_path)
            print(f'Direc Convert: {old_dir_with_full_path} ***to*** {new_dir_with_full_path}')

        order_files = order_file_list_by_ctime(root, files)
        for file_item in order_files:
            old_name_with_full_path, new_name_with_full_path = handler_action(root, file_item)
            rename_path(old_name_with_full_path, new_name_with_full_path)
            print(f'File Convert: {old_name_with_full_path} ===to==== {new_name_with_full_path}')


def rename_path(old, new):
    p = pathlib.Path(fr'{old}')
    target = pathlib.Path(fr'{new}')
    p.rename(target)
    return 0


def main():
    """
    找到排除的子目录及目录下的子文件
    对目录执行rename操作
    :return:
    """
    exclude_children = get_exclude_children(EXCLUDE_DIR)
    # 直接重命名给定子目录，而不是docs
    for path in ['💡科普', '🛠软件工具', '💻工作', '📌TODO', '💰投资理财']:
        root = full_path(ROOT_PATH, path)
        rename_path_without_exclude(root, exclude_children)


if __name__ == '__main__':
    main()
