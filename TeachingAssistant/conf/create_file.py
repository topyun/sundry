
# 下载作业文件
def download_file(full_file_path,r):
    with open(full_file_path, 'wb') as f:
        f.write(r.content)
    f.close()

# 写入文本文件
def downtext_file(statistics_path,content):
    with open(statistics_path,'a',encoding='utf-8') as f:
        f.write(content + '\n')
    f.close()

# 转换cookie
def cookie_to_dict(cookie):
    cookie_dict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        cookie_dict[key] = value
    return cookie_dict
