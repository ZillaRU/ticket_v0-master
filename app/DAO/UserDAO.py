from app.DAO.create_schema import User, Connection


def add_user(new_user):
    conn = Connection()
    try:
        conn = Connection()
        conn.add(new_user)
        conn.commit()
        conn.close()
        print('[db]:新增用户成功')
    except:
        conn.rollback()
        print('[db]:rollback add_user')


def edit_user(user_id, new_user):
    conn = Connection()
    try:
        conn = Connection()
        user=conn.query(User).filter_by(user_id=user_id).first()
        user.password = new_user.password
        user.tel = new_user.tel
        conn.commit()
        conn.close()
        print('[db]:修改用户信息成功')
    except:
        conn.rollback()
        print('[db]:rollback edit_user')


def find_user(name):
    conn = Connection()
    the_user=conn.query(User).filter_by(user_name=name).first()
    conn.commit()
    conn.close()
    return the_user