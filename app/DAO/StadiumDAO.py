from app.DAO.create_schema import Stadium, Connection


def add_a_stadium(stadium):
    conn = Connection()
    try:
        conn.add(stadium)
        conn.commit()
        conn.close()
        print('[db]:新增场馆信息成功')
    except:
        conn.rollback()
        print('[db]:rollback add_a_stadium')


def delete_a_stadium(stadium_id):
    conn = Connection()
    try:
        conn = Connection()
        stadium = conn.query(Stadium).filter_by(stadium_id=stadium_id).first()
        conn.delete(stadium)
        conn.commit()
        conn.close()
        return '[db]:删除场馆信息成功'
    except:
        conn.rollback()
        return '[db]:rollback delete_stadium'


def find_stadiums_by_city(city):
    conn = Connection()
    stadiums_in_city = conn.query(Stadium.stadium_id,Stadium.stadium_name,Stadium.address,Stadium.has_seats,Stadium.pic_src)\
        .filter_by(city=city)\
        .all()
    conn.close()
    return stadiums_in_city


def find_all_stadiums():
    conn = Connection()
    all_stadiums = conn.query(Stadium.stadium_id,Stadium.stadium_name,Stadium.city,Stadium.address,Stadium.has_seats,Stadium.pic_src)\
        .all()
    conn.close()
    return all_stadiums


def edit_a_stadium(stadium_id, new_stadium):
    conn = Connection()
    try:
        stadium = conn.query(Stadium).filter_by(stadium_id=stadium_id).first()
        stadium.stadium_name = new_stadium.stadium_name
        stadium.city = new_stadium.city
        stadium.address = new_stadium.address
        stadium.has_seats = new_stadium.has_seats
        stadium.pic_src = new_stadium.pic_src
        conn.commit()
        conn.close()
        print('[db]:更新场馆信息成功')
    except:
        conn.rollback()
        print('[db]:rollback edit_stadium')
