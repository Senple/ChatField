# coding:utf-8
import json
import csv
import os
from datetime import datetime
from bottle import route, run, template, request, response, redirect, static_file


@route("/")
def sample():
    # print("HELLO WORLD")
    return redirect("/chat_room")
# # @route("/static/<filepath:re:.*\.css>")
# # def css(filepath):
# #     return static_file(filepath, root="static")


@route("/chat_room")
def chat_room():
    """
    チャットを行う画面
    :return:
    """
    talk_list = get_talk()
    username = "user"
    return template("sample",username=username, talk_list=talk_list)

def get_talk():
    """
    永続化されたチャットデータを取得する関数
    CSVからリスト形式でデータを取得している
    :return:
    """
    talk_list = []
    # 履歴ファイルがない場合は空ファイルを作成する
    if not os.path.exists("./chat_history.csv"):
        # chat_data.csv→chat_history.csv
        open("./chat_history.csv", "w").close()

    with open('./chat_history.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            talk_list.append({
                "talk_time": row[0],
                "username": row[1],
                "content": row[2],
                #chat_data→content
                })
    # try:
    #     if talk_list[-1]["content"] == "Hi":
    #         print("OK")
    #     elif talk_list[-1]["content"] == "おはよう":
    #         print("NOOOOO")
    # except IndexError:
    #     print("Lack of data maybe")
    return talk_list

@route('/static/<file_path:path>')
def static(file_path):
    """
    静的ファイル専用のルーティング
    /static/* は静的ファイルが存在するものとして動く
    :param file_path:
    :return:
    """
    return static_file(file_path, root="./static")


@route("/talk", method="POST")
def talk():
    """
    発言を登録し、チャットルームへリダイレクトします
    :return:
    """

    # マルチバイトデータのためgetではなくgetunicodeにする
    content = request.forms.getunicode("chat_word")
    username = "user"
    # 発言時間取得
    talk_time = datetime.now()
    greeting_list = ["おはよう","こんにちは","こんにちわ","Hi","hi","こんばんは","こんばんわ"]

    if content in greeting_list:
        greeting = greet()
        new_data =  greeting
    elif content == "削除":
        new_data = "やめてくりー"
    else:
        new_data = "その言葉はまだわかんないんだ！ ごめんねm(__)m"
    # 発言保存
    save_talk(talk_time, username, content, new_data)

    return redirect("/chat_room")

def greet():
    now = datetime.now()
    greet_list = ["もしかして…夜明け待ちですか","おはよう","こんにちは","こんばんは","夜更かしはだめですよ~"]
    time = now.hour
    if time <= 5 and time > 3:
        return greet_list[0]
    elif time <=  9 and time >5:
        return greet_list[1]
    elif time <= 17 and time > 9:
        return greet_list[2]
    elif time <=20 and time > 17:
        return greet_list[3]
    else:
        return greet_list[4]

@route("/api/talk", method=["GET", "POST"])
def talk_api():
    """
    発言一覧を管理するAPI
     GET -> 発言一覧を戻す
    POST -> 発言を保存する
     json eg.
     [
        {
            talk_time:2016-09-17 15:00:49.937402
            username:sayamada
            content:おはよう
        }
    :
        },
        {
            talk_time:2016-09-17 15:58:03.200027
            username:sayamada
            content:こんにちは
        },
        {
            talk_time:2016-09-17 15:58:12.289631
            username:sayamada
            content:元気ですか？
        }
     ]
     :return:
    """
    if request.method == "GET":
        talk_list = get_talk()
        return json.dumps(talk_list)
    elif request.method == "POST":
        # マルチバイトデータのためgetではなくgetunicodeにする
        content = request.forms.getunicode("chat_word")
        # 発言者をcookieから取得
        username = "user"
        # 発言時間取得
        talk_time = datetime.now()
        # 発言保存
        greeting_list = ["おはよう","こんにちは","こんにちわ","Hi","hi","こんばんは","こんばんわ"]

        if content in greeting_list:
            greeting = greet()
            new_data =  greeting
        elif content == "削除":
            new_data = "やめてくりー"
        else:
            new_data = "その言葉はまだわかんないんだ！ ごめんねm(__)m"
        save_talk(talk_time, username, content, new_data)
        return json.dumps({
         "status": "success"
        })

def save_talk(talk_time, username, content, new_data):
    """
    チャットデータを永続化する関数
    CSVとしてチャットの内容を書き込んでいる

    :param talk_time:
    :param username:
    :param content:
    :return:
    """
    # print("why save_talk!")

    with open('./chat_history.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([talk_time, username,content])
        if new_data != "null":
            writer.writerow([talk_time, "bot", new_data])


# サーバの起動
run(host='localhost', port=8080, debug=True, reloader=True)
