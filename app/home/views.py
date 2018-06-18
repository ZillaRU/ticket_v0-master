from flask import render_template, request, session
from app.DAO.UserDAO import add_user, find_user
from app.DAO.create_schema import User
from app.home.forms import RegisterForm, LoginForm
from . import home


# 用户注册 路由叫 /register会莫名404 神奇...
@home.route('/signIn', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('html_page/register.html', form=form)
    else:
        if form.validate_on_submit():
            print('用户提交数据通过格式验证，提交的值为：', form.data)
            new_user = User(
                user_name=form.username.data,
                password=form.password.data,
                tel=form.tel.data,
                id_card=form.idCard.data
            )
            add_user(new_user)
            return '注册成功'
        else:
            return render_template('html_page/register.html', form=form)


@home.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('html_page/login.html', form=form)
    else:
        form = LoginForm()
        if form.validate_on_submit():
            print('用户提交数据通过格式验证，提交的值为：', form.data)
            user = find_user(form.username.data)
            if not user:
                return '无效的用户名'
            elif user.password == form.password.data:
                session['username'] = request.form['username']
                return '登录成功'
        else:
            return render_template('html_page/login.html', form=form)


@home.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if request.method == 'GET':
        return render_template('html_page/search.html', form=form)
    else:
        print(form.data)
        return redirect(url_for('home.shows',
                        stadium_name=form.stadium.data,
                        city=form.city.data,
                        artist=form.artist.data,
                        show_title=form.show_title.data))


@home.route('/shows', methods=['GET', 'POST'])
def shows():
    if request.method == 'GET':
        stadium_name = request.args.get('stadium_name')
        city = request.args.get('city')
        artist = request.args.get('artist')
        show_title = request.args.get('show_title')
        if stadium_name=='':
            stadium_name='none'
        if city=='':
            city='none'
        if show_title=='':
            show_title='none'
        if artist=='':
            artist='none'
        return render_template('html_page/shows.html',stadium_name=stadium_name,
                               city=city,artist=artist,show_title=show_title)


@home.route('/getRes/<int:page>/<string:city>/<string:stadium>/<string:artist>/<string:show_name>', methods=['GET', 'POST'])
def get_res(page,city,stadium,artist,show_name):
    print('getRes')
    data = None
    if city != 'none':
        data = p_find_shows_by_city(city,page)
    elif artist != 'none':
        sta = p_find_shows_by_artist(artist,page)
    elif stadium != 'none':
        data = p_find_shows_by_stadium(stadium,page)
    elif show_name != 'none':
        data = p_find_shows_by_name(show_name,page)
    else:
        data = p_find_all_shows(page)
    data_dict = {}
    shows_status='has shows'
    if len(data) == 0:
        shows_status = 'no shows'
    ret = 'SUCCESS'
    if data is None:
        ret = 'FAILURE'
    data_dict['shows_status'] = shows_status
    data_dict['shows_list'] = data
    res = {'api': 'getRes', 'ret': ret, 'data': data_dict}
    return json.dumps(res, ensure_ascii=False)


# 用户主页
@home.route('/')
def index():
    return "hello from home"
