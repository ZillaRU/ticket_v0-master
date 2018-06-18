from flask import render_template, request, session, redirect, url_for, json

from app.DAO.AreaDAO import *
from app.DAO.ArtistDAO import *
from app.DAO.ShowsDAO import *
from app.DAO.ShowsSessionDAO import *
from app.DAO.StadiumDAO import *
from app.DAO.UserDAO import *
from app.DAO.create_schema import *
from app.admin.forms import *
from app.home.forms import *
from . import admin


# 管理员主页
@admin.route('/')
def index():
    return 'admin,hello'


# 注册 路由叫 /register会莫名404 神奇...
@admin.route('/signIn', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    # POST
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
        return render_template('register.html', form=form)


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    # POST
    if form.validate_on_submit():
        print('用户提交数据通过格式验证，提交的值为：', form.data)
        user = find_user(form.username.data)
        if not user:
            return '无效的用户名'
        elif user.password == form.password.data:
            session['username'] = request.form['username']
            return '登录成功'
    else:
        return render_template('login.html', form=form)


@admin.route('/addStadium',methods=['GET', 'POST'])
def add_stadium():
    if request.method == 'GET':
        form = StadiumForm()
        return render_template('admin/addStadium.html', form=form)
    # POST
    else:
        form = StadiumForm()
        if form.validate_on_submit():
            if form.picSrc.data != '':
                pic_file = stadiumImgs.save(form.picSrc.data)
            new_stadium = Stadium(
                stadium_name=form.stadiumName.data,
                city=form.city.data,
                address=form.address.data,
                has_seats=form.hasSeats.data
            )
            if form.picSrc.data != '':
                new_stadium.pic_src = form.picSrc.data.filename
            add_a_stadium(new_stadium)
            return redirect(url_for('admin.view_stadiums'))
        else:
            return render_template('admin/addStadium.html', form=form)


@admin.route('/viewStadiums', methods=['GET','POST'])
def view_stadiums():
    if request.method == 'GET':
        form=StadiumForm()
        return render_template('admin/viewStadiums.html', form=form)
    if request.method == 'POST':
        form = StadiumForm()
        if form.validate_on_submit():
            if form.picSrc.data != '':
                pic_file = stadiumImgs.save(form.picSrc.data)
            new_stadium = Stadium(
                stadium_name=form.stadiumName.data,
                city=form.city.data,
                address=form.address.data,
                has_seats=form.hasSeats.data
            )
            if form.picSrc.data != '':
                new_stadium.pic_src = form.picSrc.data.filename
            edit_a_stadium(form.stadiumId.data, new_stadium)
            return redirect(url_for('admin.view_stadiums'))


@admin.route('/getStadiums', methods=['GET'])
def get_stadiums():
    print('get_stadiums')
    stadium_list = find_all_stadiums()
    # print(stadium_list)
    data_dict = {}
    stadium_status='has stadiums'
    if len(stadium_list) == 0:
        stadium_status = 'no stadium'
    ret = 'SUCCESS'
    if stadium_list is None:
        ret = 'FAILURE'
    data_dict['stadium_status'] = stadium_status
    data_dict['stadium_list'] = stadium_list
    res = {'api': 'getStadiums', 'ret': ret, 'data': data_dict}
    return json.dumps(res, ensure_ascii=False)
    # return render_template('html_page/admin/view_stadiums.html')


@admin.route('/addShow/<string:city>', methods=['GET', 'POST'])
def add_show(city):
    sta_list = find_stadiums_by_city(city)
    form = ShowForm()
    form.stadiumId.choices = [(sta.stadium_id, sta.stadium_name) for sta in sta_list]
    if request.method == 'GET':
        # print(form.stadiumId.choices)
        return render_template('admin/addShow.html', form=form)
    else:
        print(form.stadiumId.choices)
        print(form.stadiumId.data)
        if form.validate_on_submit():
            if form.showPic.data != '':
                pic_file = showImgs.save(form.showPic.data)
            if form.descriptionFile.data != '':
                desc_file = showDescFiles.save(form.descriptionFile.data)
            show = Shows(
                show_name=form.showName.data,
                producer=form.producer.data,
                stadium_id=form.stadiumId.data,
                can_choose_seats=form.canChooseSeats.data
                   )
            if form.showPic.data != '':
                show.show_pic = form.showPic.data.filename
            if form.descriptionFile.data != '':
                show.description_file = form.descriptionFile.data.filename
            add_a_show(show)
            return redirect(url_for('admin.view_shows'))
        else:
            return render_template("admin/addShow.html", form=form)


@admin.route('/viewShows', methods=['GET', 'POST'])
def view_shows():
    sta_list = find_all_stadiums()
    form = ShowForm()
    form.stadiumId.choices = [(sta.stadium_id, sta.stadium_name) for sta in sta_list]
    if request.method == 'GET':
        return render_template('admin/viewShows.html',form=form)
    else:
        if form.validate_on_submit():
            if form.showPic.data != '':
                pic_file = showImgs.save(form.showPic.data)
            if form.descriptionFile.data != '':
                pic_file = showDescFiles.save(form.descriptionFile.data)
            new_show = Shows(
                show_name=form.showName.data,
                producer=form.producer.data,
                stadium_id=form.stadiumId.data,
                can_choose_seats=form.canChooseSeats.data
            )
            if form.showPic.data != '':
                new_show.show_pic = form.showPic.data.filename
            if form.descriptionFile.data != '':
                new_show.description_file = form.descriptionFile.data.filename
            edit_show_info(form.showId.data, new_show)
            return redirect(url_for('admin.view_shows'))


@admin.route('/getShows', methods=['GET', 'POST'])
def get_shows():
    show_list = find_all_shows()
    # print(stadium_list)
    data_dict = {}
    shows_status = 'has shows'
    ret = 'SUCCESS'
    if show_list is None:
        ret = 'FAILURE'
    if len(show_list) == 0:
        shows_status = 'no shows'
    data_dict['shows_status'] = shows_status
    data_dict['shows_list'] = show_list
    res = {'api': 'getShows', 'ret': ret, 'data': data_dict}
    return json.dumps(res, ensure_ascii=False)
    # return render_template('html_page/admin/viewShows.html', show_json=json.dumps(res, ensure_ascii=False))


# 传入了show_id
@admin.route('/addSession/<int:show_id>', methods=['GET', 'POST'])
def add_session(show_id):
    # session_id = len(find_session_by_show(show_id))+1
    num=max_session_by_show(show_id)
    if num[0] is None:
        session_id = 1
    else:
        session_id = num[0] +1
    print(session_id)
    form = SessionForm()
    if request.method == 'GET':
        form.show_id.data = show_id
        return render_template('admin/addSession.html', form=form)
    else:
        if form.validate_on_submit():
            new_session = ShowSession(
                show_id=show_id,
                session_id=session_id,
                start_time=form.start_time.data,
                sale_time=form.sale_time.data,
                end_sale_time=form.end_sale_time.data,
                limit=form.limit.data
                   )
            add_a_session(new_session)
            return redirect(url_for('admin.view_sessions', show_id=show_id))
        else:
            return render_template("admin/addSession.html", form=form)


# # 传入了show_id
# @admin.route('/addSession/<int:show_id>', methods=['GET', 'POST'])
# def add_session(show_id):
#     show_id = request.args.get('show_id')
#     session_id = len(find_session_by_show(show_id))+1
#     # print(count_session_by_show(show_id))
#     print(session_id)
#     form = SessionAddForm()
#     if request.method == 'GET':
#         return render_template('html_page/admin/addSession.html', form=form)
#     else:
#         if form.validate_on_submit():
#             new_session = ShowSession(
#                 show_id=show_id,
#                 session_id=session_id,
#                 start_time=form.start_time.data,
#                 sale_time=form.sale_time.data,
#                 end_sale_time=form.end_sale_time.data
#                    )
#             add_a_session(new_session)
#             return redirect(url_for('admin.view_session',show_id=show_id))
#         else:
#             return render_template("html_page/admin/addSession.html", form=form)


# @admin.route('/viewSessions/<int:show_id>',methods=['GET', 'POST'])
# def view_sessions(show_id):
#     form = SessionAddForm()
#     if request.method == 'GET':
#         return render_template('html_page/admin/viewSessions.html', form=form)
#     else:
#         if form.validate_on_submit():
#             new_sess = ShowSession(
#                 start_time=form.start_time.data,
#                 sale_time=form.sale_time.data,
#                 end_sale_time=form.end_sale_time.data,
#                 limit=form.limit.data
#             )
#             edit_a_session(form.show_id.data,form.session_id.data, new_sess)
#             return redirect(url_for('admin.view_sessions',show_id=show_id))
#
#
#     # return render_template('html_page/admin/viewSessions.html')


@admin.route('/viewSessions', methods=['GET', 'POST'])
def view_sessions():
    show_id = request.args.get('show_id')
    form = SessionForm()
    if request.method == 'GET':
        return render_template('admin/viewSessions.html', show_id=show_id, form=form)
    else:
        if form.validate_on_submit():
            new_sess = ShowSession(
                start_time=form.start_time.data,
                sale_time=form.sale_time.data,
                end_sale_time=form.end_sale_time.data,
                limit=form.limit.data
            )
            edit_a_session(form.show_id.data,form.session_id.data, new_sess)
        else:
            return '表单验证未通过'
        # return redirect(url_for('admin.view_sessions',show_id=show_id))
        return render_template('admin/viewSessions.html',show_id=show_id,form=form)


@admin.route('/getSessions/<int:show_id>', methods=['GET', 'POST'])
def get_sessions(show_id):
    sess_list = find_session_by_show(show_id)
    # print(stadium_list)
    data_dict = {}
    ret = 'SUCCESS'
    if sess_list is None:
        ret = 'FAILURE'
    session_status = 'has session'
    if len(sess_list) == 0:
        session_status = 'no session'
    data_dict['session_status'] = session_status
    data_dict['session_list'] = sess_list
    res = {'api': 'viewSession', 'ret': ret, 'data': data_dict}
    return json.dumps(res, ensure_ascii=False)


@admin.route('/addArtist',methods=['GET', 'POST'])
def add_artist():
    if request.method == 'GET':
        form = ArtistForm()
        return render_template('admin/addArtist.html', form=form)
    # POST
    else:
        form = ArtistForm()
        if form.validate_on_submit():
            if form.artist_pic.data != '':
                pic_file = artistImgs.save(form.artist_pic.data)
            new_art = Artist(artist_name=form.artist_name.data)
            if form.artist_pic.data != '':
                new_art.artist_pic = form.artist_pic.data.filename
            add_an_artist(new_art)
            return redirect(url_for('admin.view_artists'))
        else:
            return render_template('admin/addArtist.html', form=form)


@admin.route('/viewArtists', methods=['GET','POST'])
def view_artists():
    if request.method == 'GET':
        form=ArtistForm()
        return render_template('admin/manageArtists.html', form=form)
    if request.method == 'POST':
        form = ArtistForm()
        if form.validate_on_submit():
            if form.artist_pic.data != '':
                pic_file = artistImgs.save(form.artist_pic.data)
            new_art = Artist(artist_name=form.artist_name.data)
            if form.artist_pic.data != '':
                new_art.artist_pic = form.artist_pic.data.filename
            edit_an_artist(form.artist_id.data, new_art)
            return redirect(url_for('admin.view_artists'))


@admin.route('/getArtists', methods=['GET'])
def get_artists():
    print('get_artists')
    art_list = find_all_artists()
    # print(stadium_list)
    data_dict = {}
    artist_status='has artists'
    if len(art_list) == 0:
        artist_status = 'no artists'
    ret = 'SUCCESS'
    if art_list is None:
        ret = 'FAILURE'
    data_dict['artist_status'] = artist_status
    data_dict['artist_list'] = art_list
    res = {'api': 'getArtists', 'ret': ret, 'data': data_dict}
    return json.dumps(res, ensure_ascii=False)
    # return render_template('html_page/admin/view_stadiums.html')


@admin.route('/addArea/<int:stadium_id>', methods=["GET", "POST"])
def add_area(stadium_id):
    if request.method == 'GET':
        form = AreaForm()
        form.stadium_id.data = stadium_id
        return render_template('admin/addArea.html', form=form)
    # POST
    else:
        form = AreaForm()
        # area_id=len(find_areas_by_stadium(form.stadium_id.data))+1
        num=get_max_area_id(form.stadium_id.data)
        if num[0] is None:
            area_id = 1
        else:
            area_id = num[0] + 1
        if form.validate_on_submit():
            new_area = Area(
                stadium_id=form.stadium_id.data,
                area_id=area_id,
                area_name=form.area_name.data,
                coordinate=str(form.x1.data)+','+str(form.y1.data)+'|'+str(form.x2.data)+','+str(form.y2.data),
                row_count=form.row_count.data,
                col_count=form.col_count.data
            )
            message=add_an_area(new_area)
            return render_template('admin/viewAreas.html', form=AreaForm(),stadium_id=stadium_id,message=message)
        else:
            return '数据格式验证未通过'


@admin.route('/viewAreas',methods=["GET", "POST"])
def view_areas():
    if request.method == 'GET':
        stadium_id = request.args.get('stadium_id')
        print(stadium_id)
        form = AreaForm()
        return render_template('admin/viewAreas.html', form=form, stadium_id=stadium_id)
    if request.method == 'POST':
        form = AreaForm()
        if form.validate_on_submit():
            new_a = Area(
                area_name=form.area_name.data,
                coordinate=str(form.x1.data)+','+str(form.y1.data)+'|'+str(form.x2.data)+','+str(form.y2.data),
                row_count=form.row_count.data,
                col_count=form.col_count.data
            )
            edit_an_area(form.stadium_id.data,form.area_id.data, new_a)
        else:
            return "validate_on_submit failed"
        return render_template('admin/viewAreas.html',form=AreaForm(),stadium_id=request.args.get('stadium_id'))


@admin.route('/getAreas', methods=['GET'])
def get_areas():
    print('get_areas')
    stadium_id = request.args.get('stadium_id')
    print(stadium_id)
    area_list = find_areas_by_stadium(stadium_id)
    print(area_list)
    data_dict = {}
    area_status='has areas'
    if len(area_list) == 0:
        area_status = 'no area'
    ret = 'SUCCESS'
    if area_list is None:
        ret = 'FAILURE'
    data_dict['area_status'] = area_status
    data_dict['area_list'] = area_list
    res = {'api': 'getAreas', 'ret': ret, 'data': data_dict}
    return json.dumps(res, ensure_ascii=False)


@admin.route('/deleteStadium',methods=['GET'])
def delete_stadium():
    print('delete_stadium')
    stadium_id = request.args.get('stadium_id')
    return render_template('admin/viewStadiums.html',
                           form=StadiumForm(),message=delete_a_stadium(stadium_id))


@admin.route('/deleteArtist',methods=['GET'])
def delete_artist():
    print('delete_artist')
    artist_id = request.args.get('artist_id')
    return render_template('admin/manageArtists.html',
                           form=ArtistForm(), message=delete_an_artist(artist_id))


@admin.route('/deleteShow',methods=['GET'])
def delete_show():
    print('delete_show')
    sta_list = find_all_stadiums()
    form = ShowForm()
    form.stadiumId.choices = [(sta.stadium_id, sta.stadium_name) for sta in sta_list]
    show_id = request.args.get('show_id')
    message = delete_a_show(show_id)
    return render_template('admin/viewShows.html',
                           form=form,message=message)


@admin.route('/deleteSession',methods=['GET'])
def delete_session():
    print('delete_session')
    form = SessionForm()
    show_id = request.args.get('show_id')
    session_id=request.args.get('session_id')
    message = delete_a_session(show_id,session_id)
    return render_template('admin/viewSessions.html',show_id=show_id,form=form,message=message)


@admin.route('/deleteArea',methods=['GET'])
def delete_area():
    print('delete_area')
    form = AreaForm()
    stadium_id = request.args.get('stadium_id')
    area_id=request.args.get('area_id')
    message = delete_an_area(stadium_id,area_id)
    return render_template('admin/viewAreas.html',stadium_id=stadium_id,form=form,message=message)
