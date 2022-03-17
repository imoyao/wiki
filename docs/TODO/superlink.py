#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2018/7/5 10:42
import re
import urllib2
from lxml import etree


def load_page(url):
    """爬取页面，分段返回字典"""
    ua_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
    req = urllib2.Request(url, headers=ua_header)
    html = urllib2.urlopen(req).read()

    with open('./static/rawhtml.html', 'w') as f:
        f.write(html)
    """
    with open('./static/rawhtml.html') as f:
        html = f.read()
    """

    h_dicts = dict()
    no_order_dicts = dict()
    li_dicts = dict()
    # 解析html 为 HTML ⽂档
    selector = etree.HTML(html)
    links = selector.xpath('//article[@class="markdown-body entry-content"]/ul/li/a/@href')
    links_text = selector.xpath('//article[@class="markdown-body entry-content"]/ul/li/a/text()')
    little_links = selector.xpath('//article[@class="markdown-body entry-content"]/ul/li/ul/li/a/@href')
    little_links_text = selector.xpath('//article[@class="markdown-body entry-content"]/ul/li/ul/li/a/text()')
    no_order_links = selector.xpath('//article[@class="markdown-body entry-content"]/ul/li/ul/li/ul/li/a/@href')
    no_order_text = selector.xpath('//article[@class="markdown-body entry-content"]/ul/li/ul/li/ul/li/a/text()')
    h_dicts = make_title_link_obj(links_text, links, obj_type='head')
    li_dicts = make_title_link_obj(little_links_text, little_links, obj_type='order')
    no_order_dicts = make_title_link_obj(no_order_text, no_order_links, obj_type='no_order')
    return h_dicts, li_dicts, no_order_dicts


def make_title_link_obj(titles, links, obj_type='head'):
    """
    组装字典
    :param titles:标题
    :param links:链接
    :param obj_type:标题类型
    :return:
    """
    content_obj = dict()
    global url
    title_links = dict(zip(titles, links))
    # print(title_links)
    ti_li_obj = {title: ''.join([url, link]) for title, link in title_links.items()}
    content_obj['content'] = ti_li_obj
    content_obj['type'] = obj_type
    return content_obj


def turn2md_line(content_obj):
    """
    把字典组装成md的超链接形式
    :param title_link_obj:
    :return:
    """
    title_link_obj = 'content' in content_obj and content_obj['content']
    obj_type = 'type' in content_obj and content_obj['type']
    count = 1
    md_lis = []
    for title, link in title_link_obj.items():
        real_title = ''.join(['[', title, ']'])
        real_link = ''.join(['(', link, ')'])
        if obj_type == 'head':
            md_line = ''.join(['## ', real_title, real_link, '\n'])
        elif obj_type == 'order':
            encode_title = real_title.encode('utf-8') if isinstance(real_title, unicode) else real_title
            re_obj = re.split(r"\[|\]| ", encode_title)
            num, title = re_obj[1], re_obj[2]
            md_line = ''.join([num, '. ', '[', title, ']', real_link, '\n'])
        elif obj_type == 'no_order':
            encode_title = real_title.encode('utf-8') if isinstance(real_title, unicode) else real_title
            re_obj = re.split(r"\[|\]| ", encode_title)
            print re_obj
            num, title = re_obj[-3], re_obj[-2] or ''
            if num and num.isdigit():
                md_line = ''.join(['- ', num, '. ', '[', title, ']', real_link, '\n'])
            else:
                md_line = ''.join(['- ', real_title, real_link, '\n'])
        count += 1
        md_lis.append(md_line)
    return md_lis


def fix2strlist(obj):
    md_ret = turn2md_line(obj)
    fix2strsqe = [line.encode('utf-8') if isinstance(line, unicode) else line for line in md_ret]
    return fix2strsqe


def main(url):
    """
    注意，由于html页面不是很规范，里面对应关系有点问题
    :param url:
    :return:
    """
    h_obj, ul_obj, li_obj = load_page(url)
    h = fix2strlist(h_obj)
    ul = fix2strlist(ul_obj)
    li = fix2strlist(li_obj)
    with open('./static/mymd.md', 'w') as f:
        f.write("\n####### this is h ########\n")
        f.writelines(h)
        f.write("\n######## this is ul #######\n")
        f.writelines(ul)
        f.write("\n******* this is li ********\n")
        f.writelines(li)


if __name__ == '__main__':
    url = 'https://github.com/taizilongxu/interview_python'
    main(url)
