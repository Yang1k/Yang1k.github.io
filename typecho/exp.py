import pymysql
import os
import re
import time, datetime



#获取所有文件路径
def get_filepath(file_dir):
    file_path = []
    for root,dirs,files in os.walk(file_dir):
        for name in files:
            file_path.append(os.path.join(root,name))
    return file_path

# 获取文件内容
def get_data(file_name):
    f = open(file_name,'r',encoding='UTF-8')
    data = f.read().split('<!--more-->')
    filestr = '<!--markdown-->' + data[1]
    pattern_time = '[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}'
    pattern_title = 'title(.*)?date'
    title_data = data[0].replace('\n','').replace(': ','')

    t = re.findall(pattern_time,title_data)
    title = re.findall(pattern_title,title_data)

    timeArray = time.strptime(t[0]+' 23:40:00', "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))

    result = [filestr.replace("'",'\''),timeStamp,title[0]]
    return result
# 获取时间
def get_time():
    pass

# 插入数据库
def insert(data):
    db = pymysql.connect("localhost","root","root","typecho")
    cursor = db.cursor()
    r = pymysql.escape_string(data[0])
    # print('insert INTO typecho_contents(title,created,modified,text,type,status,allowComment,allowFeed,allowPing,authorId) VALUES ("%s","%s","%s","%s,"post","publish",1,1,1,1) '%(data[2],data[1],data[1],r))
    cursor.execute('insert INTO typecho_contents(title,created,modified,text,type,status,allowComment,allowFeed,allowPing,authorId) VALUES ("%s","%s","%s","%s","post","publish",1,1,1,1) '%(data[2],data[1],data[1],r))
    db.commit()
    db.close()

def go():
    pass


if __name__ == '__main__':
    file_dir = './post'
    file_name_list = get_filepath(file_dir)
    for i in file_name_list:
        print(i)
        data = get_data(i)
    # r = pymysql.escape_string(data[0])
    # print(r)
        insert(data)

     


