# -*- coding:utf-8 -*-
"""
"""
__date__ = "2018/5/7"
__author__ = "zhaojm"

import sys
import json
import codecs


if __name__ == "__main__":
    config_path = sys.argv[1]
    index = sys.argv[2]

    print(config_path)


    j = None

    with codecs.open(config_path, mode='rb', encoding='utf8') as f:

        j = json.load(f)
        j['playerAddr'] = 'f4:5c:89:c0:7f:' + hex(int(index) + 16)[2:]
        j['windowName'] = 'player' + index


    with codecs.open(config_path, mode='wb', encoding='utf8') as f:
        json.dump(j, f)


