# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      ${NAME}
   Description :
   Author :         ${USER}
   date：           ${DATE}
-------------------------------------------------
   Change Activity:
                    ${DATE}:
-------------------------------------------------
"""
__author__ = '${USER}'



#################### 中台处理 ###############################
def compose_message( dataframe ):

    str0 = ("近日发布项目列表如下：\n")

    text = str0 + str(dataframe)
    return text



import requests


import os
import sys
abspath = os.path.abspath(sys.argv[0])
os.chdir(os.path.dirname(abspath)) # 切换到脚本所在目录执行
print("cd " + os.getcwd())

import sqlite3

def query_db():
    """
    后台状态检查，返回数据库检索结果
    """
    try:
        dbconn = sqlite3.connect("income.db") # 数据库文件与脚本文件在同一目录下
    except sqlite3.Error as ex:
        print(ex)
        return None
    
    try:
        dbcur=dbconn.cursor()
        #sql脚本
        sqlcmd1 = "SELECT name FROM sqlite_master WHERE type='table';"
        dbcur.execute(sqlcmd1)
        dbres = dbcur.fetchall()
        
        sqlcmd = "SELECT name,open_time,close_time,description,url FROM weain"
        dbcur.execute(sqlcmd)
        dbres = dbcur.fetchall()
        if len(dbres) > 0:
            print(" SQL OK")
    except sqlite3.Error as ex:
        print(ex)
        dbres = None
    finally:
        dbcur.close()
        dbconn.close()
        return dbres

################################# 前台处理 ##########################
import wxpy

bot = wxpy.api.bot.Bot(cache_path=True)
friends = bot.friends(update=True)
friends.pop(0)

def send_message():
    """
    执行动作：检查数据库更新 -> 组织消息 -> 查找好友 -> 发送消息 -> 反馈本人
    """
    data = query_db() #  检查是否有新数据
    if data is None:
        return
    
    text = compose_message(data)

    my_friends = []
    found = friends.search('张伟') # 好友的微信昵称，或者你存取的备注
    my_friends.append(wxpy.utils.tools.ensure_one(found))
    print(my_friends)
    for friend in my_friends:
        try:
            # friend.send(fetch_weather(friend.city))
            friend.send(text)
        except:
            print("向微信好友 " + friend + " 发送失败！\n")
    
    bot.file_helper.send('发送完毕') # 发送成功通知我

import threading
def execute_task():
    """
    调度任务：周期执行
    """
    send_message()
 
    t = threading.Timer(3600, execute_task) # 每86400秒（1天），发送1次
    t.start()


if __name__ == "__main__":
    execute_task()
