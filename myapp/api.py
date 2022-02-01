from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from flask import Blueprint

from myapp import db
from myapp.extensions import SQLAlchemyDataBase


api = Blueprint('api', __name__)
dbase = SQLAlchemyDataBase(db)


@api.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'mode' in request.form:
            session['mode'] = request.form['mode']
        elif 'num' in request.form:
            if request.form['num'].isdecimal():
                session['num'] = int(request.form['num'])
                words = dbase.get_words(session['num'])

                if not words:
                    session.pop('num')
                    flash('Ошибка: Словаря с таким номером не существует.', category='error')
                    return redirect('/#popup-dictionary')
                else:
                    session['words'] = words
                    session['n'] = 0
            else:
                flash('Ошибка: Разрешено вводить только цифры.', category='error')
                return redirect('/#popup-dictionary')

        elif 'translate' in request.form:
            if session['answer'] == request.form['translate'].lower():
                flash('Верно.', category='success')
                if session['n'] < len(session['words']) - 1:
                    session['n'] += 1
                else:
                    random.shuffle(session['words'])
                    session['n'] = 0
                return redirect(url_for('api.index'))
            else:
                flash('Wrong.', category='error')

    if 'mode' in session:
        mode = session['mode']
    else:
        mode = ''

    if 'num' in session:
        num = session['num']
        words = session['words']
        n = session['n']

        if mode == 'English-Russian':
            session['ask'] = words[n][0]
            session['answer'] = words[n][1]

        elif mode == 'Russian-English':
            session['ask'] = words[n][1]
            session['answer'] = words[n][0]

        else:
            session['ask'] = ''
            session['answer'] = ''

        ask = session['ask']
        answer = session['answer']
        hint = answer[:2]
        if ', ' in ask:
            answer = answer[:-1]

    else:
        num = ''
        ask = ''
        answer = ''
        hint = ''

    return render_template('index.html', mode=mode, num=num, ask=ask, hint=hint,
                           answer=answer)

@api.route('/add_words', methods=['POST', 'GET'])
def add_words():
    if request.method == 'POST':
        if 'ctr_num' in request.form:
            if request.form['ctr_num'].isdecimal():
                crt_num = int(request.form['ctr_num'])
                if not dbase.check_existence(crt_num):
                    dbase.create_dict(crt_num)
                    flash('Словать под номером "' + crt_num + '" создан.',
                          category='success')
                else:
                    flash("Словарь с таким именем уже существует", category='error')
            else:
                flash('Ошибка: Разрешено вводить только цифры.', category='error')
                return redirect('/add_words#popup-create-dictionary')

        elif 'num' in request.form:
            if request.form['num'].isdecimal():
                session['num'] = request.form['num']
                words = dbase.get_words(session['num'])
                session['words'] = words
                session['n'] = 0
                if not dbase.check_existence(session['num']):
                    session.pop('num')
                    flash('Словаря с таким номером не существует.', category='error')
                    return redirect('/add_words#popup-dictionary')
            else:
                flash('Ошибка: Разрешено вводить только цифры.', category='error')
                return redirect('/add_words#popup-dictionary')

    if 'num' in session:
        num = session['num']
        if 'eng' in request.form and 'rus' in request.form:
            if not dbase.check_limit(num):
                eng = request.form['eng']
                rus = request.form['rus']
                if not dbase.check_existence(eng):
                    dbase.add_word(num, eng, rus)
                    flash('Слово успешно добавлено', category='success')
                else:
                    flash('Слово уже существует.', category='error')
            else:
                flash('Количество слов в словаре достигло предела.', category='error')

    else:
        num = ''

    return render_template('add_words.html', num=num)
