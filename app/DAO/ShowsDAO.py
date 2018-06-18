from app.DAO.create_schema import Shows, Connection, Stadium


def add_a_show(new_show):
    conn = Connection()
    try:
        conn.add(new_show)
        conn.commit()
        conn.close()
        print('[db]:新增演出信息成功')
    except:
        conn.rollback()
        print('[db]:rollback add_a_show')


def delete_a_show(show_id):
    conn = Connection()
    try:
        show = conn.query(Shows).filter_by(show_id=show_id).first()
        conn.delete(show)
        conn.commit()
        conn.close()
        return '[db]:删除演出信息成功'
    except:
        conn.rollback()
        return '[db]:rollback delete_a_show'


def find_all_shows():
    conn = Connection()
    try:
        shows = conn.query(Shows.show_id,Shows.show_name,Shows.show_type,Shows.show_pic,Shows.producer,Shows.stadium_id,Shows.can_choose_seats,Shows.description_file)\
            .all()
        conn.close()
        return shows
    except:
        print('[db]: find_all_shows failed')
        return None


def find_shows_by_city(city):
    conn = Connection()
    try:
        shows = conn.query(Shows.show_id,Shows.show_name,Shows.show_type,Shows.show_pic,Shows.producer,Shows.stadium_id,Shows.can_choose_seats,Shows.description_file)\
            .join(Stadium)\
            .filter_by(city=city).all()
        conn.close()
        return shows
    except:
        print('[db]: find_shows_by_city failed')
        return None


def find_shows_by_stadium(stadium_id):
    conn = Connection()
    try:
        shows = conn.query(Shows.show_id,Shows.show_name,Shows.show_type,Shows.show_pic,Shows.producer,Shows.can_choose_seats,Shows.description_file)\
            .filter_by(stadium_id=stadium_id)\
            .all()
        conn.close()
        return shows
    except:
        print('[db]: find_shows_by_stadium failed')
        return None


def edit_show_info(show_id, new_show):
    conn = Connection()
    try:
        show = conn.query(Shows).filter_by(show_id=show_id).first()
        show.show_name = new_show.show_name
        show.show_type = new_show.show_type
        show.producer = new_show.producer
        show.show_pic = new_show.show_pic
        show.desc_file_name = new_show.desc_file_name
        show.stadium_id = new_show.stadium_id
        show.can_choose_seats = new_show.can_choose_seats
        conn.commit()
        conn.close()
        print('[db]:更新演出信息成功')
    except:
        conn.rollback()
        print('[db]:rollback edit_show_info')


# todo aaaaaa
def find_detail_by_show_id(show_id):
    conn = Connection()
    try:
        shows = conn.query(Shows.show_id,Shows.show_name,Shows.show_type,Shows.show_pic,Shows.producer,Shows.can_choose_seats,Shows.description_file)\
            .join(Stadium).filter_by(show_id=show_id)\
            .all()
        conn.close()
        return shows
    except:
        print('[db]: find_shows_by_stadium failed')
        return None


# def edit_show_detail(show_id, desc_file_name):
#     conn = Connection()
#     try:
#         show = conn.query(Stadium).filter_by(show_id=show_id).first()
#         show.desc_file_name = desc_file_name
#         conn.commit()
#         conn.close()
#         print('[db]:更新演出描述成功')
#     except:
#         conn.rollback()
#         print('[db]:rollback edit_show_detail')
