from flask import Flask, render_template, redirect, request, session, abort
# Flask - главный класс для создания экземпляра приложения
# render_template - функция для отображения HTML-шаблонов
# redirect - функция для перенаправления пользователя на другой URL
# request - объект, содержащий всю информацию о входящем HTTP-запросе
# session - хранение данных пользователя между HTTP-запросами
# abort - функция прерывания обработки запроса и возврата HTTP-ошибки клиенту
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
# flask-login - расширение для Flask, упрощающее реализацию аутентификации и управления сессиями пользователей
# LoginManager - главный класс для настройки системы аутентификации в приложении
# login_user - функция для авторизации пользователя в сесссию, делая его текущим авторизованным пользователем
# logout_user - функция для выхода пользователя из системы
# current_user - глобальный  объект, предоставляющий доступ к текущему авторизованному пользователю
# login_required - декоратор для защиты маршрутов - разрешает доступ только авторизованным пользователям
from data.jobs import Jobs
from data.users import User
from data import db_session
from data.login_form import LoginForm
from forms.jobs_form import JobForm
from forms.user import RegisterForm

app = Flask(__name__)
# создание экземпляра веб-приложения Flask
# __name__ - имя текущего модуля, если скрипт запускается напрямую, то __name__ принимает значение '__main__', иначе имя файла
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# config - словарь, где хранятся все настройки приложения Flask

login_manager = LoginManager()
# создание экземпляра 'диспетчера' системы аутентификации
login_manager.init_app(app)
# init_app() - метод, предназначеннный для инициализации

@login_manager.user_loader
def load_user(user_id):
    # user_id передается автоматически (он сохраняется в сессии Flask при вызове login_user(user))
    db_sess = db_session.create_session()
    # создание новой сессии работы с базой данных
    return db_sess.get(User, user_id)
    # возврат пользователя из БД User (поиск по айди), иначе - None

@app.route('/')
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        # current_user - глобальная переменная, текущий пользователь
        # is_authenticated - атрибут UserMixin
        jobs = db_sess.query(Jobs).filter(
            (Jobs.user == current_user) | (Jobs.is_private != True)
        )
    else:
        jobs = db_sess.query(Jobs).filter(Jobs.is_private != True)
    return render_template('index.html', jobs=jobs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
    # true, если запрос - POST, все формы прошли валидацию
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # login_user() - функция из Flask-Login
            # remember=form.remember_me.data - если в форме отмечена галочка, сессия сохранится дольше
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message='Введенные пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form, message='Пользователь с введенной почтой уже существует')
        user = User(
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
# функция logout() выполнится только для авторизованных пользователей
def logout():
    logout_user()
    # функция, удаляющая айди, очищающая куки, устанавливающая current_user в анонимное состояние
    return redirect("/")

@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = Jobs()
        news.job = form.job.data
        news.work_size = form.work_size.data
        news.collaborators = form.collaborators.data
        news.end_date = form.end_date.data
        news.is_finished = form.is_finished.data
        news.is_private = form.is_private.data
        current_user.jobs.append(news)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости', form=form)

@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
        if news:
            form.job.data = news.job
            form.work_size.data = news.work_size
            form.collaborators.data = news.collaborators
            form.end_date.data = news.end_date
            form.is_finished.data = news.is_finished
            form.is_private.data = news.is_private
        else:
            abort(404)
            # страница не найдена
    else:
        db_sess = db_session.create_session()
        news = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
        if news:
            news.job = form.job.data
            news.work_size = form.work_size.data
            news.collaborators = form.collaborators.data
            news.end_date = form.end_date.data
            news.is_finished = form.is_finished.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Редактирование новости', form=form)

@app.route('/news_delete/<int:id>')
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

def main():
    db_session.global_init("db/mars_explorer.db")
    # функция global_init из db_session
    app.run(debug=True)
    # запуск и отладка сервера

if __name__ == '__main__':
    main()
