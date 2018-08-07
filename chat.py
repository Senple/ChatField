# coding:utf-8
import csv
import os
from datetime import datetime
from bottle import route, run, template, request, response, redirect



@route("/")
def index():
    username = 0
    return template("index")


@route("/enter", method=["POST"])
def enter():
    """
    入室処理を行います。
    フォームの情報をcookieに格納し、チャット時の名前として使用します。
    :return:
    """
    # POSTデータの確認
    username = request.POST.get("username")
    print("POST username is ", username)
    # cookieへの格納
    response.set_cookie("username", username)
    return redirect("/chat_room")


@route("/chat_room")
def chat_room():
    """
    チャットを行う画面
    :return:
    """
    # cookieからの取得はrequestから行う
    username = request.get_cookie("username")
    # cookieにユーザ情報がない場合は入室画面へ戻す
    if not username:
        return redirect("/")
    # 永続化してあるこれまでのチャット履歴を取得
    talk_list = get_talk()
    return template("chat_room", username=username, talk_list=talk_list)


@route("/talk", method=["POST"])
def talk():

    """
    発言を登録し、チャットルームへリダイレクトします
    :return:
    """

    # マルチバイトデータのためgetではなくgetunicodeにする
    chat_data = request.POST.getunicode("chat")
    # 発言者をcookieから取得
    username = request.get_cookie("username")
    # 発言時間取得
    talk_time = datetime.now()

    if chat_data == "削除":
        new_data = "やめてくりー"
    elif chat_data == "こんにちは":
        new_data = 'こんにちは、{}さん'.format(username)
    else:
        new_data = "その言葉はまだわかんないんだ！ ごめんねm(__)m"
    # 発言保存
    save_talk(talk_time, username, chat_data, new_data)

    return redirect("/chat_room")


def save_talk(talk_time, username, chat_data, new_data):
    """
    チャットデータを永続化する関数
    CSVとしてチャットの内容を書き込んでいる

    :param username:
    :param chat_data:
    :param talk_time:
    :return:
    """

    with open('./chat_data.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([talk_time, username, chat_data])
        if new_data != "null":
            writer.writerow([talk_time, "bot", new_data])


def get_talk():
    """
    永続化されたチャットデータを取得する関数
    CSVからリスト形式でデータを取得している
    :return:
    """
    talk_list = []

    # 履歴ファイルがない場合は空ファイルを作成する
    if not os.path.exists("./chat_data.csv"):
        open("./chat_data.csv", "w").close()

    with open('./chat_data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            talk_list.append({
                "talk_time": row[0],
                "username": row[1],
                "chat_data": row[2],
                })
    # print(talk_list[-1])
    if talk_list[-1]["chat_data"] == "Hi":
        print("OK")
    elif talk_list[-1]["chat_data"] == "おはよう":
        print("NOOOOO")
    return talk_list

# サーバの起動
run(host='localhost', port=8080, debug=True, reloader=True)
