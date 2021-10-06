import requests
'''
r = requests.get('https://www.baidu.com/')
print(type(r))
print(r.status_code)

print(type(r.text))
#print(r.text)
print(r.cookies)

print(type(r.headers), r.headers)
#print(type(r.cookies), r.cookies)
print(type(r.url), r.url)
print(type(r.history), r.history)


#比如访问这个网址
#http://httpbin.org/get?name=germey&age=22

data = {
    'name': 'germey',
    'age': 22
}
r = requests.get("http://httpbin.org/get", params=data)
print(r.text)

#Request URL: https://you.163.com/item/detail?id=3993102&_stat_area=1&_stat_referer=search&_stat_query=%E7%8F%A0&_stat_count=56&_stat_searchversion=vecg_model-2.3
#Request Method: GET
{
id=3993102
_stat_area=1
_stat_referer=search
_stat_query=%E7%8F%A0
_stat_count=56
_stat_searchversion=vecg_model-2.3

}



header={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br', #编码
        'accept-language': 'zh-CN,zh;q=0.9',  #返回语言
        'cache-control': 'max-age=0', #缓存到期时间 0
        'upgrade-insecure-requests': '1', #加载 http 资源时自动替换成 https 请求
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}


##二进制
r = requests.get("https://github.com/favicon.ico")
with open('favicon.ico', 'wb') as f:
    f.write(r.content)


'''
#------------------------------------------------------------获得判断状态码 -----------------------------
'''

#r = requests.get('http://www.jianshu.com')
#exit() if not r.status_code == requests.codes.ok else print('Request Successfully')

#requests.codes.xxxx

# 信息性状态码
100: ('continue',),
101: ('switching_protocols',),
102: ('processing',),
103: ('checkpoint',),
122: ('uri_too_long', 'request_uri_too_long'),

# 成功状态码
200: ('ok', 'okay', 'all_ok', 'all_okay', 'all_good', '\\o/', '✓'),
201: ('created',),
202: ('accepted',),
203: ('non_authoritative_info', 'non_authoritative_information'),
204: ('no_content',),
205: ('reset_content', 'reset'),
206: ('partial_content', 'partial'),
207: ('multi_status', 'multiple_status', 'multi_stati', 'multiple_stati'),
208: ('already_reported',),
226: ('im_used',),

# 重定向状态码
300: ('multiple_choices',),
301: ('moved_permanently', 'moved', '\\o-'),
302: ('found',),
303: ('see_other', 'other'),
304: ('not_modified',),
305: ('use_proxy',),
306: ('switch_proxy',),
307: ('temporary_redirect', 'temporary_moved', 'temporary'),
308: ('permanent_redirect',
      'resume_incomplete', 'resume',), # These 2 to be removed in 3.0

# 客户端错误状态码
400: ('bad_request', 'bad'),
401: ('unauthorized',),
402: ('payment_required', 'payment'),
403: ('forbidden',),
404: ('not_found', '-o-'),
405: ('method_not_allowed', 'not_allowed'),
406: ('not_acceptable',),
407: ('proxy_authentication_required', 'proxy_auth', 'proxy_authentication'),
408: ('request_timeout', 'timeout'),
409: ('conflict',),
410: ('gone',),
411: ('length_required',),
412: ('precondition_failed', 'precondition'),
413: ('request_entity_too_large',),
414: ('request_uri_too_large',),
415: ('unsupported_media_type', 'unsupported_media', 'media_type'),
416: ('requested_range_not_satisfiable', 'requested_range', 'range_not_satisfiable'),
417: ('expectation_failed',),
418: ('im_a_teapot', 'teapot', 'i_am_a_teapot'),
421: ('misdirected_request',),
422: ('unprocessable_entity', 'unprocessable'),
423: ('locked',),
424: ('failed_dependency', 'dependency'),
425: ('unordered_collection', 'unordered'),
426: ('upgrade_required', 'upgrade'),
428: ('precondition_required', 'precondition'),
429: ('too_many_requests', 'too_many'),
431: ('header_fields_too_large', 'fields_too_large'),
444: ('no_response', 'none'),
449: ('retry_with', 'retry'),
450: ('blocked_by_windows_parental_controls', 'parental_controls'),
451: ('unavailable_for_legal_reasons', 'legal_reasons'),
499: ('client_closed_request',),

# 服务端错误状态码
500: ('internal_server_error', 'server_error', '/o\\', '✗'),
501: ('not_implemented',),
502: ('bad_gateway',),
503: ('service_unavailable', 'unavailable'),
504: ('gateway_timeout',),
505: ('http_version_not_supported', 'http_version'),
506: ('variant_also_negotiates',),
507: ('insufficient_storage',),
509: ('bandwidth_limit_exceeded', 'bandwidth'),
510: ('not_extended',),
511: ('network_authentication_required', 'network_auth', 'network_authentication')
'''

#如果想判断结果是不是404状态，可以用requests.codes.not_found来比对。
#https://zhuanlan.zhihu.com/p/33876717



#------------------------------------上传文件-----------------------------------#
'''
import requests

files = {'file': open('favicon.ico', 'rb')}
r = requests.post("http://httpbin.org/post", files=files)
print(r.text)
'''
#------------------------------------上传文件-----------------------------------#


#------------------------------------------cookies-------------------------------#
'''
import requests

r = requests.get("https://www.baidu.com")
print(r.cookies)
for key, value in r.cookies.items():
    print(key + '=' + value)
'''


'''
import requests

headers = {
    'Cookie': 'SESSIONID=ocP3RPc4od5S6BeHAb9Oxk8mS2f8DpcfDYCKDs1HqCR; JOID=UVsXA09fiylT6R9gO1yMcHj2MdYrfKkIdM08Qhp7qAtyzjtDGQxa3g_uHmM9Uz5azPY1PQOaYnFsY5BclmjiTnQ=; osd=WlgUA01UiCpT6xRjOFyOe3v1MdQgf6oIdsY_QRp5owhxzjlIGg9a3ATtHWM_WD1ZzPQ-PgCaYHpvYJBenWvhTnY=; _zap=36276637-b8d2-47fa-a097-f7e8c27af453; d_c0="AKBeg9clsRGPTjWR75KG3i1Y0P6zC5t2d3k=|1596725965"; _ga=GA1.2.1911345193.1596727689; z_c0="2|1:0|10:1606752580|4:z_c0|92:Mi4xbXZIN0JRQUFBQUFBb0Y2RDF5V3hFU1lBQUFCZ0FsVk5RMmV5WUFCR2pMdHU4UVQxbmtmY04zcUlQc1VMRzF1UjJR|ea2fb5706cc30f283c2d82b702370d34a75ffec90e0d79c47abbaeb61da88a20"; __utma=51854390.1911345193.1596727689.1606923652.1606923652.1; __utmz=51854390.1606923652.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/51745620; __utmv=51854390.100--|2=registration_date=20170919=1^3=entry_date=20170919=1; _xsrf=17d70d05-9145-4f88-8dc6-a6e04a88c976; q_c1=c68f53e0728d4197b4601a642c1981f6|1609498841000|1606752886000; KLBRSID=81978cf28cf03c58e07f705c156aa833|1609691639|1609688785; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1609504697,1609640399,1609681366,1609691897; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1609691897',
    'Host': 'www.zhihu.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}
r = requests.get('https://www.zhihu.com', headers=headers)
print(r.text)
'''

import requests

cookies = 'SESSIONID=ocP3RPc4od5S6BeHAb9Oxk8mS2f8DpcfDYCKDs1HqCR; JOID=UVsXA09fiylT6R9gO1yMcHj2MdYrfKkIdM08Qhp7qAtyzjtDGQxa3g_uHmM9Uz5azPY1PQOaYnFsY5BclmjiTnQ=; osd=WlgUA01UiCpT6xRjOFyOe3v1MdQgf6oIdsY_QRp5owhxzjlIGg9a3ATtHWM_WD1ZzPQ-PgCaYHpvYJBenWvhTnY=; _zap=36276637-b8d2-47fa-a097-f7e8c27af453; d_c0="AKBeg9clsRGPTjWR75KG3i1Y0P6zC5t2d3k=|1596725965"; _ga=GA1.2.1911345193.1596727689; z_c0="2|1:0|10:1606752580|4:z_c0|92:Mi4xbXZIN0JRQUFBQUFBb0Y2RDF5V3hFU1lBQUFCZ0FsVk5RMmV5WUFCR2pMdHU4UVQxbmtmY04zcUlQc1VMRzF1UjJR|ea2fb5706cc30f283c2d82b702370d34a75ffec90e0d79c47abbaeb61da88a20"; __utma=51854390.1911345193.1596727689.1606923652.1606923652.1; __utmz=51854390.1606923652.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/51745620; __utmv=51854390.100--|2=registration_date=20170919=1^3=entry_date=20170919=1; _xsrf=17d70d05-9145-4f88-8dc6-a6e04a88c976; q_c1=c68f53e0728d4197b4601a642c1981f6|1609498841000|1606752886000; KLBRSID=81978cf28cf03c58e07f705c156aa833|1609691639|1609688785; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1609504697,1609640399,1609681366,1609691897; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1609691897'
jar = requests.cookies.RequestsCookieJar()
headers = {
    'Host': 'www.zhihu.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
for cookie in cookies.split(';'):
    key, value = cookie.split('=', 1)
    jar.set(key, value)
r = requests.get("http://www.zhihu.com", cookies=jar, headers=headers)
print(r.text)