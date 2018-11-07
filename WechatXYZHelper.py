# -*- coding:utf-8 -*-
# 微信小宇宙助手
import datetime
import re
import time
import random
import json
import itchat
from itchat.content import *
from apscheduler.schedulers.blocking import BlockingScheduler

# 群聊人员列表
member_python_list_1 = []
member_python_list_2 = []
member_android_list = []
member_speak_list = []
member_guy_list = []

# 加群人员的列表
group_python_list_1 = []  # Python 1群
group_python_list_2 = []  # Python 2群
group_android_list = []  # Android 群
group_speak_list = []  # 闲聊 群
group_guy_list = [] # 公号读者 群

# 获取群聊人员的列表的正则
nickname_compile = re.compile(r"\<ChatroomMember:.*?'NickName': '(.*?)'", re.S)

# 获取群聊名称的正则
group_name_compile = re.compile("'NickName': '(.{1,40})', 'HeadImgUrl':", re.S)

# 添加好友通过欢迎词
welcome_words = '(˶ᵔᵕᵔ˶)嘤嘤嘤，😘😘😘\n我是智障机器人小Pig，发送关键字：「菜单」 \n 查看更多小Pig的更多功能！'

# 菜单回复词
menu_answer = '(˶ᵔᵕᵔ˶)锵锵锵~🎉🎉🎉，\n' \
              '可用关键词如下（输入对应数字，比如1）：\n' \
              ' 🐷 1.加入「Python学习交流群」\n' \
              ' 🐷 2.加入「Android学习交流群」\n' \
              ' 🐷 3.加入「闲聊扯淡群」\n' \
              ' 🐷 4.加入「抠腚男孩的妙妙屋」\n' \
              ' 🐷 5.关注公众号「抠腚男孩」\n' \
              ' 🐷 6.小猪的「个人博客」\n' \
              ' 🐷 7.小猪的「GitHub」\n' \
              ' 🐷 8.给小猪「打赏」\n' \
              ' 🐷 9.小猪的「微信」（不闲聊哦~）\n' \
              '注：请不要回复过于频繁，智障机器人不会聊天哦！🐶'

# 加群统一回复词
add_group_answer = '🚫🚫🚫FBI Warning!🚫🚫🚫\n(｀･ω･´)ゞ非常抱歉的通知您：\n\n微信粑粑把拉人接口禁掉了，你的加群请求已收到，小猪童鞋会尽快把你拉到群中。\n\nヾﾉ≧∀≦)o 麻烦耐心等候哦！'

# 重复加群回复词
add_repeat_answer = '<(｀^´)>哼，敲生气，你都在群里了，加什么群鸭！😠😠😠'

# 捐献回复词
donate_answer = '(˶ᵔᵕᵔ˶)您的打赏，会让小猪更有动力肝♂出更Interesting的文章，谢谢支持～😊😊😊'

# 小猪回复词
pig_answer = '(˶ᵔᵕᵔ˶)小猪童鞋不闲聊哦，有问题欢迎到群里讨论哦~'

# 404回复词
no_match_answer = '！！！非常抱歉，您输入的关键词粗错了，请发送「菜单」查看支持的数字关键字ヽ(･ω･´ﾒ)'


# 自动通过加好友
@itchat.msg_register(itchat.content.FRIENDS)
def deal_with_friend(msg):
    itchat.add_friend(**msg['Text'])  # 自动将新好友的消息录入，不需要重载通讯录
    time.sleep(random.randint(1, 3))
    itchat.send_msg(welcome_words, msg['RecommendInfo']['UserName'])
    time.sleep(random.randint(1, 3))
    itchat.send_image('welcome.png', msg['RecommendInfo']['UserName'])


# 自动回复配置
@itchat.msg_register([TEXT])
def deal_with_msg(msg):
    text = msg['Content']
    if text == u'菜单':
        time.sleep(random.randint(1, 3))
        itchat.send(menu_answer, msg['FromUserName'])
    # 加入Python交流群
    elif text == u'1':
        time.sleep(random.randint(1, 3))
        nickname = msg['User']['NickName']
        if nickname not in member_python_list_1 and nickname not in member_python_list_2:
            itchat.send_msg("【" + nickname + "】童鞋\n" + add_group_answer, msg['FromUserName'])
            if nickname is not None:
                # 人数超过阀值拉入二群
                if len(member_python_list_1) >= 495:
                    if nickname not in group_python_list_2:
                        group_python_list_2.append(nickname)
                else:
                    if nickname not in group_python_list_1:
                        group_python_list_1.append(nickname)
        else:
            itchat.send_msg(add_repeat_answer, msg['FromUserName'])
    # 加入Android交流群
    elif text == u'2':
        time.sleep(random.randint(1, 3))
        nickname = msg['User']['NickName']
        if nickname not in member_android_list:
            itchat.send_msg("【" + nickname + "】童鞋\n" + add_group_answer, msg['FromUserName'])
            if nickname is not None and nickname not in group_android_list:
                group_android_list.append(nickname)
        else:
            itchat.send_msg(add_repeat_answer, msg['FromUserName'])
    # 加入闲聊群
    elif text == u'3':
        time.sleep(random.randint(1, 3))
        nickname = msg['User']['NickName']
        if nickname not in member_speak_list:
            itchat.send_msg("【" + nickname + "】童鞋\n" + add_group_answer, msg['FromUserName'])
            if nickname is not None and nickname not in group_speak_list:
                group_speak_list.append(nickname)
        else:
            itchat.send_msg(add_repeat_answer, msg['FromUserName'])
    # 加入公号读者群
    elif text == u'4':
        time.sleep(random.randint(1, 3))
        nickname = msg['User']['NickName']
        if nickname not in member_guy_list:
            itchat.send_msg("【" + nickname + "】童鞋\n" + add_group_answer, msg['FromUserName'])
            if nickname is not None and nickname not in group_guy_list:
                group_guy_list.append(nickname)
        else:
            itchat.send_msg(add_repeat_answer, msg['FromUserName'])
    # 公众号
    elif text == u'5':
        time.sleep(random.randint(1, 3))
        itchat.send_image('gzh.jpg', msg['FromUserName'])
    # 个人博客
    elif text == u'6':
        time.sleep(random.randint(1, 3))
        return 'coder-pig的个人主页-掘金：https://juejin.im/user/570afb741ea493005de84da3'
    # GitHub
    elif text == u'7':
        time.sleep(random.randint(1, 3))
        return 'https://github.com/coder-pig'
    # 打赏
    elif text == u'8':
        time.sleep(random.randint(1, 3))
        itchat.send_image('ds.gif', msg['FromUserName'])
        time.sleep(random.randint(1, 3))
        itchat.send_msg(donate_answer, msg['FromUserName'])
        time.sleep(random.randint(1, 3))
        itchat.send_image('wxpay.png', msg['FromUserName'])
    # 小猪微信
    elif text == u'9':
        time.sleep(random.randint(1, 3))
        itchat.send_msg(pig_answer, msg['FromUserName'])
        time.sleep(random.randint(1, 3))
        itchat.send_image('scan_code.png', msg['FromUserName'])
    # 其他默认回复：
    else:
        time.sleep(random.randint(1, 3))
        itchat.send_image('hrwh.png', msg['FromUserName'])
        time.sleep(random.randint(1, 3))
        itchat.send_msg(no_match_answer, msg['FromUserName'])


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
            elif group_name == '技♂术交流🈲':
                member_speak_list.clear()
                results = nickname_compile.findall(str(msg))
                for result in results:
                    member_speak_list.append(result)
            elif group_name == '抠腚男孩的妙妙屋':
                member_guy_list.clear()
                results = nickname_compile.findall(str(msg))
                for result in results:
                    member_guy_list.append(result)


# 发送加群人信息列表
def send_friend_group():
    friend_dict = {"Python": [], "Android": [], "Speak": [], "Python2": [], "Guy":[]}
    for p in group_python_list_1:
        friend_dict['Python'].append(p)
    for a in group_android_list:
        friend_dict['Android'].append(a)
    for s in group_speak_list:
        friend_dict['Speak'].append(s)
    for p2 in group_python_list_2:
        friend_dict['Python2'].append(p2)
    for g in group_guy_list:
        friend_dict['Guy'].append(g)
    if len(friend_dict['Python']) > 0 or len(friend_dict['Android']) > 0 or len(friend_dict['Speak']) > 0 or len(
                    friend_dict['Python2']) > 0 or len(friend_dict['Guy']) > 0:
        itchat.send_msg(str(json.dumps(friend_dict, ensure_ascii=False, indent=4)), toUserName="filehelper")
        group_python_list_1.clear()
        group_python_list_2.clear()
        group_android_list.clear()
        group_speak_list.clear()
        group_guy_list.clear()


# 登陆成功后开启定时任务，每隔2个小时发送一次加群人数
def after_login():
    sched.add_job(send_friend_group, 'interval', minutes=1)
    sched.start()


# 登陆时先获取群聊的UserName，获取群成员昵称会用到
def get_member_list():
    python_chat_rooms = itchat.search_chatrooms(name='小猪的Python学习交流1群')
    if len(python_chat_rooms) > 0:
        group_username = python_chat_rooms[0]['UserName']
        result = itchat.update_chatroom(group_username, detailedMember=True)
        member_python_list_1.clear()
        results = nickname_compile.findall(str(result))
        for result in results:
            member_python_list_1.append(result)
    python_chat_rooms_2 = itchat.search_chatrooms(name='小猪的Python学习交流2群')
    if len(python_chat_rooms_2) > 0:
        group_username = python_chat_rooms_2[0]['UserName']
        result = itchat.update_chatroom(group_username, detailedMember=True)
        member_python_list_2.clear()
        results = nickname_compile.findall(str(result))
        for result in results:
            python_chat_rooms_2.append(result)
    android_chat_rooms = itchat.search_chatrooms(name='小猪的Android学习交流群')
    if len(android_chat_rooms) > 0:
        group_username = android_chat_rooms[0]['UserName']
        result = itchat.update_chatroom(group_username, detailedMember=True)
        member_android_list.clear()
        results = nickname_compile.findall(str(result))
        for result in results:
            member_android_list.append(result)
    speak_chat_rooms = itchat.search_chatrooms(name='技♂术交流🈲')
    if len(android_chat_rooms) > 0:
        group_username = speak_chat_rooms[0]['UserName']
        result = itchat.update_chatroom(group_username, detailedMember=True)
        member_speak_list.clear()
        results = nickname_compile.findall(str(result))
        for result in results:
            member_speak_list.append(result)
    guy_chat_rooms = itchat.search_chatrooms(name='抠腚男孩的妙妙屋')
    if len(android_chat_rooms) > 0:
        group_username = guy_chat_rooms[0]['UserName']
        result = itchat.update_chatroom(group_username, detailedMember=True)
        member_guy_list.clear()
        results = nickname_compile.findall(str(result))
        for result in results:
            member_guy_list.append(result)

if __name__ == '__main__':
    sched = BlockingScheduler()
    itchat.auto_login(loginCallback=get_member_list, enableCmdQR=2)
    itchat.run(blockThread=False)
    after_login()
