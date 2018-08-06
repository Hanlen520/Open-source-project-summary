#!/usr/bin/python
# coding=utf-8
'''
Created on Aug 06, 2018
author = "xwatson"
python = 3.6.4
version = 1.0
'''


import os
import sys
import requests
from lxml import etree
from urllib.parse import urljoin
# 导入自定义模块
sys.path.append(os.path.dirname(os.getcwd()))
from tools_unit import ToolsUnit


# 清理fork项目
class CleanForkProject(object):

    def __init__(self):
        self.result = None
        self.self_cookies = None
        self.session = None
        self.github_url = "https://github.com/"
        self.xzsheldon_url = "xzshedon?page=1&tab=repositories"
        self.user_name = '****'    # github账号
        self.passwd = '****'   # 密码
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
                'Referer': 'https://github.com/',
                'Host': 'github.com',
                'Upgrade-Insecure-Requests': '1',
            }

    def start_script(self):
        html, payload = self.login_github()
        # 获取总页数
        total_page_tag = html.xpath("//em[@class='current']")[0]
        total_page_element = etree.tostring(total_page_tag, pretty_print=True).decode('utf-8')
        total_pages = total_page_element.split(" ")[2][-9]
        print("[+] Info: get total page: %s" % total_pages)
        i = 1
        while i <= int(total_pages):
            html = self.login_github(url="xzshedon?page=%d&tab=repositories" % i)
            block_lists = html.xpath("//li[@class='col-12 d-block width-full py-4 border-bottom public fork']")
            project_lists = html.xpath(
                "//li[@class='col-12 d-block width-full py-4 border-bottom public fork']/div[@class='d-inline-block mb-1']/h3/a")
            forked_url_lists = html.xpath(
                "//li[@class='col-12 d-block width-full py-4 border-bottom public fork']/div[@class='d-inline-block mb-1']/span/a")

            block_lists_len = len(block_lists)
            for num in range(block_lists_len):
                fork_project = project_lists[num].text.split(" ")[-1]
                fork_project_setting = "xzshedon/"+fork_project+"/settings"
                clear_url = urljoin(self.github_url, fork_project_setting)
                payload['utf8'] = True
                payload['_method:'] = 'delete'
                payload['verify'] = fork_project
                self.session.post(clear_url, headers=self.headers, data=payload)
            print("[+] Info: finish for %i page" % i)
            i += 1

    # 若没登录过，则发起登录；若session存在，则用上次的session；
    def login_github(self, url=None):
        if self.session:
            url_new = (urljoin(self.github_url, url))
            r = self.session.get(url_new, headers=self.headers)
            html = etree.HTML(r.text)
            return html
        else:
            payload = {'commit': 'Sign in', 'login': self.user_name, 'password': self.passwd}
            self.session = requests.Session()
            self.result = self.session.get(urljoin(self.github_url, "login"), headers=self.headers)
            self.self_cookies = self.result.cookies
            payload['authenticity_token'] = ToolsUnit.get_token(self.result.content)
            self.result = self.session.post(urljoin(self.github_url, "session"), headers=self.headers, data=payload)
            url = (urljoin(self.github_url, "xzshedon?tab=repositories"))
            r = self.session.get(url, headers=self.headers)
            html = etree.HTML(r.text)
            return html, payload

    def delete_project(self):
        '''
        utf8: ✓
        _method: delete
        authenticity_token: Ppuy/3dKKyYgUQT7VZolY8RoDGhiFhMpWYCLLp/ENPhBR6QrciMYpDDgnmnghMTJfZGkqDQuPQtGeNOXVY44Eg==
        verify: HelloGitHub
        :return:
        '''

        pass


if __name__ == '__main__':
    CleanForkProject().start_script()




