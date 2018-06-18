from sqlalchemy import func

from app.DAO.create_schema import Artist, Follows, Includes, Connection, Shows


def add_an_artist(new_art):
    conn = Connection()
    try:
        conn.add(new_art)
        conn.commit()
        conn.close()
        print('[db]:新增艺人成功')
    except:
        conn.rollback()
        print('[db]:rollback add_artist')


def delete_an_artist(art_id):
    conn = Connection()
    try:
        artist = conn.query(Artist).filter_by(artist_id=art_id).first()
        conn.delete(artist)
        conn.commit()
        conn.close()
        return '[db]:删除艺人成功'
    except:
        conn.rollback()
        return '[db]:rollback delete_artist'


def edit_an_artist(art_id,new_art):
    conn = Connection()
    try:
        art = conn.query(Artist).filter_by(artist_id=art_id).first()
        art.artist_name = new_art.artist_name
        art.artist_pic = new_art.artist_pic
        conn.commit()
        conn.close()
        print('[db]:编辑艺人成功')
    except:
        conn.rollback()
        print('[db]:rollback edit_an_artist')


def find_all_artists():
    conn = Connection()
    artists = conn.query(Artist.artist_id,Artist.artist_name,Artist.artist_pic).all()
    conn.close()
    return artists


def add_follow(user_id,art_id):
    conn = Connection()
    try:
        fo = Follows(user_id=user_id, artist_id=art_id)
        conn = Connection()
        conn.add(fo)
        conn.commit()
        conn.close()
        print('[db]:关注成功')
    except:
        conn.rollback()
        print('[db]:rollback add_follow')


def delete_follow(user_id,art_id):
    conn = Connection()
    try:
        fo = conn.query(Follows).filter_by(user_id=user_id,artist_id=art_id).first()
        conn.delete(fo)
        conn.commit()
        conn.close()
        print('[db]:取消关注成功')
    except:
        conn.rollback()
        print('[db]:rollback delete_follow')


def find_follows_by_user(user_id):
    conn = Connection()
    try:
        my_fo=conn.query(Follows.artist_id,Artist.artist_name)\
            .filter_by(user_id=user_id)\
            .join(Artist)
        conn.commit()
        conn.close()
        print('[db]:获取关注成功')
        return my_fo
    except:
        print('find_follows_by_user failed')
        return None


# # todo 语句有错
# def find_shows_by_follow(user_id):
#     conn = Connection()
#     try:
#         my_fo_shows=conn.query(Shows.show_id,Shows.show_name,Artist.artist_id,Artist.artist_name) \
#             .join(Includes).join(Artist).join(Follows)\
#             .filter_by(user_id=user_id).all()
#         conn.commit()
#         conn.close()
#         print('[db]:获取关注艺人演出成功')
#         return my_fo_shows
#     except:
#         print('find_shows_by_follow failed')
#         return None

# print(find_shows_by_follow(1))


def add_show_art(show_id,art_id):
    conn = Connection()
    try:
        a_s = Includes(show_id=show_id, artist=art_id)
        conn = Connection()
        conn.add(a_s)
        conn.commit()
        conn.close()
        print('[db]:新增 艺人-演出 成功')
    except:
        conn.rollback()
        print('[db]:rollback add_show_art')


def delete_show_art(show_id,art_id):
    conn = Connection()
    try:
        a_s = conn.query(Includes).filter_by(show_id=show_id,artist=art_id).first()
        conn.delete(a_s)
        conn.commit()
        conn.close()
        print('[db]:取消 艺人-演出 成功')
    except:
        conn.rollback()
        print('[db]:rollback delete_show_art')


def find_artists_by_show(show_id):
    try:
        conn = Connection()
        artists = conn.query(Artist.artist_id,Artist.artist_name,Artist.artist_pic).join(Includes)\
            .filter_by(show_id=show_id).all()
        conn.close()
        return artists
    except:
        print('find_artists_by_show failed')
        return None


def find_shows_by_artist(artist_id):
    try:
        conn = Connection()
        shows = conn.query(Shows.show_id,Shows.show_name,Shows.show_type,Shows.producer,Shows.stadium_id,Shows.can_choose_seats,Shows.description_file)\
            .join(Includes)\
            .filter_by(artist=artist_id)\
            .all()
        conn.close()
        return shows
    except:
        print('find_shows_by_artist failed')
        return None


# find_follow_by_user
def find_follow_by_user(user_id):
    try:
        conn = Connection()
        follows = conn.query(Artist.artist_id,Artist.artist_name).join(Follows)\
            .filter_by(user_id=user_id)\
            .all()
        conn.close()
        return follows
    except:
        print('find_follow_by_user failed')
        return None


# count_follow_by_artist
def count_follow_by_artist(artist_id):
    conn = Connection()
    count = conn.query(func.count(Follows.user_id))\
        .filter_by(artist_id=artist_id).first()
    conn.close()
    return count

# add_follow
# delete_follow
# add_artist
# delete_artist
# add_artist_to_show