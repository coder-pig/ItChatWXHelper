# -*- coding:utf-8 -*-
# 微信机器人
import datetime
import re
import time
import random
import json
import itchat
from itchat.content import *
from apscheduler.schedulers.blocking import BlockingScheduler

# 获取群聊人员的列表的正则
nickname_compile = re.compile(r"\<ChatroomMember:.*?'NickName': '(.*?)'", re.S)

# 获取群聊名称的正则
group_name_compile = re.compile("'NickName': '(.{1,40})', 'HeadImgUrl':", re.S)

# 添加好友通过欢迎词：
welcome_words = '(˶ᵔᵕᵔ˶)嘤嘤嘤，😘😘😘\n我是智障机器人小Pig，发送关键字：「菜单」 \n 查看更多小Pig的更多功能！'

# 重复加群回复词
add_repeat_answer = '<(｀^´)>哼，敲生气，你都在群里了，加什么群鸭！😠😠😠'

# 捐献回复词
donate_answer = '(˶ᵔᵕᵔ˶)您的打赏，会让小猪更有动力肝♂出更Interesting的文章，谢谢支持～😊😊😊'

# 404回复词
no_match_answer = '！！！非常抱歉，您输入的关键词粗错了，请发送「菜单」查看支持的数字关键字ヽ(･ω･´ﾒ)'

# 群聊信息
group_infos_list = [
    {'name': '小猪的Python学习交流1群', 'id': '', 'count': 0, 'members': []},
    {'name': '小猪的Python学习交流2群', 'id': '', 'count': 0, 'members': []},
    {'name': '小猪的Android学习交流群', 'id': '', 'count': 0, 'members': []},
    {'name': '抠腚男孩的妙妙屋', 'id': '', 'count': 0, 'members': []},
]

# 聊天次数(限制一个用户只能交互10次，避免有些沙雕一直刷回复)
user_chat_statistics = {}

# 所有群聊id列表
group_id_list = []

# 群聊人员列表
member_python_list_1 = []  # Python 1群
member_python_list_2 = []  # Python 2群
member_android_list = []  # Android 群
member_guy_list = []  # 闲聊群


# 自动通过加好友
@itchat.msg_register(itchat.content.FRIENDS)
def deal_with_friend(msg):
    itchat.add_friend(**msg['Text'])  # 自动将新好友的消息录入，不需要重载通讯录
    time.sleep(random.randint(1, 3))
    itchat.send_msg(welcome_words, msg['RecommendInfo']['UserName'])
    time.sleep(random.randint(1, 3))
    itchat.send_image('welcome.png', msg['RecommendInfo']['UserName'])


# 菜单回复词
menu_answer = '(˶ᵔᵕᵔ˶)锵锵锵~🎉🎉🎉，\n' \
              '可用关键词（输入数字触发）：\n' \
              '1️⃣「抠腚男孩」公众号\n' \
              '2️⃣「Python」加群\n' \
              '3️⃣「Android」加群\n' \
              '4️⃣「闲聊」加群\n' \
              '5️⃣「个人博客」\n' \
              '6️⃣「GitHub」\n' \
              '7️⃣「打赏」\n' \
              '注：智障机器人不会聊天哦，请勿回复过于频繁。🐶'


# 自动回复配置
@itchat.msg_register([TEXT])
def deal_with_msg(msg):
    name = msg['FromUserName']
    if name not in user_chat_statistics:
        user_chat_statistics[name] = 0
    chat_count = user_chat_statistics.get(name)
    if chat_count < 11:
        user_chat_statistics[name] += 1
        text = msg['Content']
        if text == u'菜单':
            time.sleep(random.randint(1, 3))
            itchat.send(menu_answer, msg['FromUserName'])
        # 公众号
        elif text == u'1':
            time.sleep(random.randint(1, 3))
            itchat.send_image('gzh.png', msg['FromUserName'])
        # 加入Python交流群
        elif text == u'2':
            time.sleep(random.randint(1, 3))
            nickname = msg['User']['NickName']
            if nickname not in member_python_list_1 and nickname not in member_python_list_2:
                if nickname is not None:
                    # 人数超过阀值拉入二群
                    if group_infos_list[0].get('count') >= 499:
                        itchat.add_member_into_chatroom(group_infos_list[1].get('id'),
                                                        [{'UserName': msg['FromUserName']}], useInvitation=True)
                    else:
                        itchat.add_member_into_chatroom(group_infos_list[0].get('id'),
                                                        [{'UserName': msg['FromUserName']}], useInvitation=True)
            else:
                itchat.send_msg(add_repeat_answer, msg['FromUserName'])
        # 加入Android交流群
        elif text == u'3':
            time.sleep(random.randint(1, 3))
            nickname = msg['User']['NickName']
            if nickname not in member_android_list:
                itchat.add_member_into_chatroom(group_infos_list[2].get('id'),
                                                [{'UserName': msg['FromUserName']}], useInvitation=True)
            else:
                itchat.send_msg(add_repeat_answer, msg['FromUserName'])
        # 加入公号读者群
        elif text == u'4':
            time.sleep(random.randint(1, 3))
            nickname = msg['User']['NickName']
            if nickname not in member_guy_list:
                itchat.add_member_into_chatroom(group_infos_list[3].get('id'),
                                                [{'UserName': msg['FromUserName']}], useInvitation=True)
            else:
                itchat.send_msg(add_repeat_answer, msg['FromUserName'])

        # 个人博客
        elif text == u'5':
            time.sleep(random.randint(1, 3))
            return 'coder-pig的个人主页-掘金：https://juejin.im/user/570afb741ea493005de84da3'
        # GitHub
        elif text == u'6':
            time.sleep(random.randint(1, 3))
            return 'https://github.com/coder-pig'
        # 打赏
        elif text == u'7':
            time.sleep(random.randint(1, 3))
            itchat.send_image('ds.gif', msg['FromUserName'])
            time.sleep(random.randint(1, 3))
            itchat.send_msg(donate_answer, msg['FromUserName'])
            time.sleep(random.randint(1, 3))
            itchat.send_image('wxpay.png', msg['FromUserName'])
        # 404
        else:
            time.sleep(random.randint(1, 3))
            itchat.send_msg(no_match_answer, msg['FromUserName'])


# 监听加群信息，更新群成员列表
@itchat.msg_register([NOTE], isGroupChat=True)
def revoke_msg(msg):
    result = group_name_compile.search(str(msg))
    if result is not None:
        group_name = result.group(1)
        if '邀请' in str(msg['Text']):
            results = nickname_compile.findall(str(msg))
            if group_name == '小猪的Python学习交流1群':
                member_python_list_1.clear()
                for result in results:
                    member_python_list_1.append(result)
            elif group_name == '小猪的Python学习交流2群':
                member_python_list_2.clear()
                results = nickname_compile.findall(str(msg))
                for result in results:
                    member_python_list_2.append(result)
            elif group_name == '小猪的Android学习交流群':
                member_android_list.clear()
                results = nickname_compile.findall(str(msg))
                for result in results:
                    member_android_list.append(result)
            elif group_name == '抠腚男孩的妙妙屋':
                member_guy_list.clear()
                results = nickname_compile.findall(str(msg))
                for result in results:
                    member_guy_list.append(result)


# 清空聊天次数统计
def clear_statistics():
    global user_chat_statistics
    user_chat_statistics = {}


# 登陆成功后开启定时任务，每隔12小时清空一次聊天统计
def after_login():
    sched.add_job(clear_statistics, 'interval', hours=12)
    sched.start()


# 登陆时先获取群聊的UserName
def get_member_list():
    for group in group_infos_list:
        chat_rooms = itchat.search_chatrooms(name=group.get('name'))
        if len(chat_rooms) > 0:
            # 设置群聊id
            group['id'] = chat_rooms[0]['UserName']
            # 更新群聊成员
            result = itchat.update_chatroom(group.get('id'), detailedMember=True)
            member_list = []
            results = nickname_compile.findall(str(result))
            group['count'] = len(results)
            for result in results:
                member_list.append(result)
            group['members'] = member_list


if __name__ == '__main__':
    sched = BlockingScheduler()
    itchat.auto_login(loginCallback=get_member_list, enableCmdQR=2)
    itchat.run(blockThread=False)
    after_login()
