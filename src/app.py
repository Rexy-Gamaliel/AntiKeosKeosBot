from flask import Flask, render_template, url_for, request, redirect
from flask_mysql_connector import MySQL
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE'] = 'anebo'
db = MySQL(app)
cur = db.new_cursor(dictionary=True)


class Chat():
    id: int = 0

    def __init__(self, _text):
        self.id += 1
        self.text = _text
        self.time = datetime.utcnow

    def __repr__ (self):
        return '<Chat %r : \"%r\">' %self.id %self.text
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
        chat_text = request.form['content']

        new_task = Chat(text=chat_text)

        # pass to backend

        # try:
        #     db.session.add(new_task)
        #     db.session.commit()
        #     return redirect('/')
        # except:
        #     return "Error on adding task"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id: int):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting tasks'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error updateing task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)