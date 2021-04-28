from flask import Flask, render_template, url_for, request, redirect
from inoutput import mydb, mycursor, outputBot
from datetime import datetime
app = Flask(__name__)
db = mydb
cursor = mycursor


class Chat():
    cursor.execute("SELECT MAX(id) FROM chats")
    counter: int = cursor.fetchone()[0] or 0

    def __init__(self, text: str, source: str):
        Chat.counter += 1
        self.id = Chat.counter
        self.text = text
        self.source = source
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        self.time = time

    def __repr__ (self):
        return '<Chat #{} ({}: {}): \"{}\">'.format(self.id, self.source, self.time, self.text)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_text = request.form['content']
        user_chat = Chat(text=user_text, source="user")

        # pass to backend
        bot_text = outputBot(user_text)
        bot_chat = Chat(text=bot_text, source="bot")
        try:
            query = "INSERT INTO chats(id, text, source, timeStamp) VALUES \
                    (%s, %s, %s, %s), \
                    (%s, %s, %s, %s)"
            args = (
                user_chat.id, user_chat.text, "user", user_chat.time,
                bot_chat.id, bot_chat.text, "bot", bot_chat.time
            )
            print(args)
            cursor.execute(query, args)
            db.commit()

            return redirect('/')
        except:
            return 'Ups, there\'s an error'

    else:
        query = "SELECT * FROM chats ORDER BY timeStamp asc, id asc"
        cursor.execute(query)
        chats = cursor.fetchall()
        
        return render_template("index.html", chats=preprosesChats(chats=chats))


@app.route('/how_to_use', methods=['GET', 'POST'])
def how_to_use():
    if request.method == 'POST':
        return redirect('/')
    return render_template('howtouse.html')


def preprosesChats(chats):
    dict = {}
    temp = []
    for chat in chats:
        dict.update({
            'id': chat[0],
            'text': splitText(chat[1]),
            'source': chat[2],
            'timeStamp': chat[3]
        })
        temp.append(dict.copy())
    return temp
    
def splitText(text: str):
    return text.split('\n')

if __name__ == "__main__":
    app.run(debug=True)