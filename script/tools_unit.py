#!/usr/bin/python
# coding=utf-8
'''
Created on Aug 06, 2018
author = "xwatson"
python = 3.6.4
version = 1.0
'''

import os
from lxml import etree


class ToolsUnit(object):

    def __init__(self):
        pass

    def get_token(text):
    #<input name="authenticity_token" value="Wwc+VXo2iplcjaTzDJwyigClTyZ9FF6felko/X3330UefrKyBT1f/eny1q1qSmEgFfTm0jKv+HW7rQ5hYu84Qw==" type="hidden">
        html = etree.HTML(text)
        t = html.xpath("//input[@name='authenticity_token']")
        try:
            token = t[0].get('value')
        except IndexError:
            print("[+] Error: can't get login token, exit...")
            os.exit()
        except Exception as e:
            print(e)
            os.exit()
        # print(token)
        return token