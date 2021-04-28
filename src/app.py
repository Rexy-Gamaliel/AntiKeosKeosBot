from flask import Flask, render_template, url_for, request, redirect
#from flask_mysql_connector import MySQL
#from flaskext.mysql import MySQL
#from flask_mysqldb import MySQL
#from sqlConnect import mydb, mycursor
from sqlConnect import mydb, mycursor
import sqlConnect as sqlcon
from wordSearch import interface
from datetime import datetime


app = Flask(__name__)

db = mydb
cursor = mycursor

# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_DATABASE'] = 'anebo'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_PORT'] = 5000



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
'''
CREATE TABLE Task (
id INT primary key AUTO_INCREMENT,
tanggal DATE,
kodeMatkul VARCHAR(6),
jenis VARCHAR(255),
judul VARCHAR(255)
);
'''

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_text = request.form['content']
        user_chat = Chat(text=user_text, source="user")

        # pass to backend
        bot_text = interface(user_text)
        bot_chat = Chat(text=bot_text, source="bot")
        try:
            query = "INSERT INTO chats(id, text, source, timeStamp) VALUES \
                    (%s, %s, %s, %s), \
                    (%s, %s, %s, %s)"
            args = (
                user_chat.id, user_chat.text, "user", user_chat.time,
                bot_chat.id, bot_chat.text, "bot", bot_chat.time
            )
            cursor.execute(query, args)
            db.commit()

            return redirect('/')
        except:
            return 'Ups, there\'s an error'

    else:
        query = "SELECT * FROM chats ORDER BY timeStamp asc, id asc"
        cursor.execute(query)
        chats = cursor.fetchall()
        
        return render_template("index.html", chats=chats)


@app.route('/how_to_use', methods=['GET', 'POST'])
def how_to_use():
    if request.method == 'POST':
        return redirect(-'/')
    return render_template('howtouse.html')

# @app.route('/delete/<int:id>')
# def delete(id: int):
#     task_to_delete = Todo.query.get_or_404(id)

#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'Error deleting tasks'

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)

#     if request.method == 'POST':
#         task.content = request.form['content']
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'Error updateing task'
#     else:
#         return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)