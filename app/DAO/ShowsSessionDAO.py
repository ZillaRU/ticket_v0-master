from sqlalchemy import func

from app.DAO.create_schema import Shows, Connection, ShowSession


def add_a_session(new_sess):
    conn = Connection()
    try:
        conn.add(new_sess)
        conn.commit()
        conn.close()
        print('[db]:新增场次信息成功')
    except:
        conn.rollback()
        print('[db]:rollback add_a_session')


def delete_a_session(show_id,sess_id):
    conn = Connection()
    try:
        sess = conn.query(ShowSession).filter_by(show_id=show_id,session_id=sess_id).first()
        conn.delete(sess)
        conn.commit()
        conn.close()
        return '[db]:删除场次信息成功'
    except:
        conn.rollback()
        return '[db]:rollback delete_a_session'

print(delete_a_session(5,0))

def edit_a_session(show_id, session_id, new_session):
    conn = Connection()
    try:
        sess = conn.query(ShowSession).filter_by(show_id=show_id,session_id=session_id).first()
        print(sess)
        sess.start_time = new_session.start_time
        sess.sale_time = new_session.end_sale_time
        sess.end_sale_time = new_session.end_sale_time
        sess.limit = new_session.limit
        conn.commit()
        conn.close()
        print('[db]:更新场次信息成功')
    except:
        conn.rollback()
        print('[db]:rollback edit_a_session')


def find_session_by_show(show_id):
    conn = Connection()
    sess = conn.query(ShowSession.session_id,ShowSession.show_id,ShowSession.start_time,ShowSession.sale_time,ShowSession.end_sale_time,ShowSession.limit)\
        .filter_by(show_id=show_id)\
        .all()
    conn.close()
    return sess

print(find_session_by_show(1))


# 返回的是字符串类型？？
def max_session_by_show(show_id):
    conn = Connection()
    count = conn.query(func.max(ShowSession.session_id))\
        .filter_by(show_id=show_id).first()
    conn.close()
    return count



def get_session_detail_by_id(show_id, session_id):
    conn = Connection()
    sess = conn.query(ShowSession.session_id,ShowSession.show_id,ShowSession.start_time,ShowSession.sale_time,ShowSession.end_sale_time,ShowSession.limit)\
        .filter_by(show_id=show_id, session_id=session_id)\
        .first()
    conn.close()
    return sess
