from flask import Flask, request, redirect
import sqlite3
import os

if not os.path.exists('db/tasks.db'):
    os.mknod('db/tasks.db')
    conn = sqlite3.connect('db/tasks.db')
    cursor = conn.cursor()
    with open('db/init_tasksdb') as f:
        for line in f:
            cursor.execute(line)
    with open('hello') as f:
        for i, line in enumerate(f.read().split(',')):
            print(f'INSERT INTO task4 VALUES {i+1}, {line[1:][:-1]}')
            cursor.execute(f'INSERT INTO task4 VALUES ({i+1}, {line[1:][:-1]})')
    conn.commit()
    conn.close()

if not os.path.exists('db/results.db'):
    os.mknod('db/results.db')
    conn = sqlite3.connect('db/results.db')
    cursor = conn.cursor()
    with open('db/init_resultsdb') as f:
        for line in f:
            cursor.execute(line)
    conn.commit()
    conn.close()

conn_tasks = sqlite3.connect('db/tasks.db', check_same_thread=False)
cur_tasks = conn_tasks.cursor()
conn_results = sqlite3.connect('db/results.db', check_same_thread=False)
cur_results = conn_results.cursor()
app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <a href="/task1">Task 1. Самое начало</a><br>
    <a href="/task2">Task 2. Найди меня</a><br>
    <a href="/task3">Task 3. Очень-очень длинный флаг</a><br>
    <a href="/task4">Task 4. Очень-очень большой найди меня</a><br>
    <a href="/flag">Enter your flag</a>
    '''

@app.route('/task1', methods=['GET', 'POST'])
def task1():
    html = '''
    Привет! Это первое задание.<br>
    Оно самое простое)<br>
    Вытащить флаг из таблицы 'flag'<br>
    <form method="post">
        <input name="query" placeholder="Введите запрос">
        <button type="submit">Отправить</button>
    </form>
    '''
    if request.method == 'GET':
        return html
    else:
        query = request.form.get('query')
        
        cur_tasks.execute(query)
        conn_tasks.commit()
        return html + '<div>' + str(cur_tasks.fetchall()) + '</div>'



@app.route('/task2', methods=['GET', 'POST'])
def task2():
    html = '''
    Задание второе. <br>
    В таблице <i>task2</i> где-то спрятан ключ. Найдите его)<br>
    <form method="post">
        <input name="query">
        <button type="submit">Отправить</button>
    </form>
    '''
    if request.method == 'GET':
        return html
    else:
        query = request.form.get('query')
        cur_tasks.execute(query)
        conn_tasks.commit()
        res = ''.join([f'<tr><th>{i[0]}</th><th>{i[1]}</th></tr>' for i in cur_tasks.fetchall()])
        table = f'''<table border="1"><thead><tr><th>id</th><th>flag</th></tr></thead><tbody>{res}</tbody></table>'''
        return f'{html} <br> {table}'

@app.route('/task3', methods=['GET', 'POST'])
def task3():
    html = '''
    Здрасьте. Это очень, очень длинный flag (прям
    очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень-очень
 длинный flag) <br>
    select * from: <form method="post">
        <input name="query">
        <button type="submit">Отправить</button>
    </form>
    '''
    if request.method == 'GET':
        return html
    else:
        query = request.form.get('query')

        cur_tasks.execute(f'select * from {query}')
        conn_tasks.commit()
        res = ''.join([f'<tr><th>{i[0]}</th><th>{i[1]}</th></tr>' for i in cur_tasks.fetchall()])
        table = f'''<table border="1"><thead><tr><th>price</th><th>flag</th></tr></thead><tbody>{res}</tbody></table>'''
        return f'{html} <br> {table}'

@app.route('/task4', methods=['GET', 'POST'])
def task4():
    html = '''
    Ето мильон значений, you're welcome
    <form method="post">
        <input name="query">
        <button type="submit">Отправить</button>
    </form>
    '''
    if request.method == 'GET':
        return html
    else:
        query = request.form.get('query')

        cur_tasks.execute(f'{query}')
        conn_tasks.commit()
        res = ''.join([f'<tr><th>{i[0]}</th><th>{i[1]}</th></tr>' for i in cur_tasks.fetchall()])
        table = f'''<table border="1"><thead><tr><th>price</th><th>flag</th></tr></thead><tbody>{res}</tbody></table>'''
        return f'{html} <br> <div>{table}</div>'

@app.route('/flag', methods=['GET', 'POST'])
def flag():
    if request.method == 'GET':
        cur_results.execute('''
            select * from results;
         ''')
        table = '\n'.join([f'{i[0]}: {i[1]} {i[2]} {i[3]} {i[4]}' for i in cur_results.fetchall()])
        return '''
                 <form method="post">
                     <input name="login" placeholder="Login">
                     <input name="flag" placeholder="Flag 'hack_or_go_home{flag}">
                     <button type="submit">Submit</button>
                 </form>
                 ''' + table

    else:
        login = request.form.get('login')
        key = request.form.get('flag')
        result = check(key)
        if result != 0:
            cur_results.execute(f'''
             insert or ignore into results (login, task{result}) values(?,1)
             ''', [login])
            conn_results.commit()
            cur_results.execute(f'''update results set task{result}=1 where login=?
             ''', [login])
            conn_results.commit()
        return redirect('/flag')

def check(flag):
    answers = ['hack_or_go_home{asjdlkzzc231s}',
        'hack_or_go_home{tksnbwjvty}',
        'hack_or_go_home{ya_vas_kategorichesky_privetstvuy_eto_ochen_ochen_extra_mega_ultra_acva_achy_dlinny_flag}',
        'hack_or_go_home{dogvsqrljifbaqb}'
        ]
    for i, ans in enumerate(answers):
        if flag == ans:
            return i + 1
    return 0

if __name__ == '__main__':
    app.run()
