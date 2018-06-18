from app.DAO.create_schema import *
from config import Config


def p_find_all_artists(page):
    conn = Connection()
    try:
        artists = conn.query(Artist.artist_id,Artist.artist_name,Artist.artist_pic)\
            .paginate(page, per_page=Config.per_page,error_out=False).items
        # print(artists)
        conn.close()
        return artists
    except:
        print('[db]: p_find_all_artists failed')
        return None


def p_find_shows_by_city(city,page):
    conn = Connection()
    try:
        shows = conn.query(Shows.show_id,Shows.show_name,Shows.show_pic,Shows.producer,Shows.stadium_id,Shows.can_choose_seats,Shows.description_file)\
            .join(Stadium)\
            .filter_by(city=city).paginate(page, per_page=Config.per_page,error_out=False).items
        conn.close()
        print(shows)
        return shows
    except:
        print('[db]: p_find_shows_by_city failed')
        return None


def p_find_all_shows(page):
    conn = Connection()
    try:
        shows = conn.query(Shows.show_id,Shows.show_name,Shows.show_type,Shows.show_pic,Shows.producer,Shows.stadium_id,Shows.can_choose_seats,Shows.description_file)\
            .paginate(page, per_page=Config.per_page,error_out=False).items
        conn.close()
        # print(shows)
        return shows
    except:
        print('[db]: p_find_all_shows failed')
        return None


def p_find_shows_by_stadium(stadium_name,page):
    conn = Connection()
    str="%"+stadium_name+"%"
    print(str)
    try:
        shows = conn.query(Shows.show_id,Shows.show_name,Shows.show_type,Shows.show_pic,Shows.producer,Shows.can_choose_seats,Shows.description_file)\
            .join(Stadium).filter(Stadium.stadium_name.like(str)) \
            .paginate(page, per_page=Config.per_page, error_out=False).items
        conn.close()
        return shows
    except:
        print('[db]: p_find_shows_by_stadium failed')
        return None


def p_find_shows_by_artist(art_name,page):
    conn = Connection()
    str="%"+art_name+"%"
    print(str)
    try:
        shows = conn.query(Shows.show_id,Shows.show_name,Shows.show_type,Shows.show_pic,Shows.producer,Shows.can_choose_seats,Shows.description_file)\
            .join(Includes).join(Artist).filter(Artist.artist_name.like(str)) \
            .paginate(page, per_page=Config.per_page, error_out=False).items
        conn.close()
        return shows
    except:
        print('[db]: p_find_shows_by_artist failed')
        return None


def p_find_shows_by_name(name,page):
    conn = Connection()
    str="%"+name+"%"
    print(str)
    try:
        shows = conn.query(Shows.show_id,Shows.show_name,Shows.show_type,Shows.show_pic,Shows.producer,Shows.can_choose_seats,Shows.description_file)\
            .filter(Shows.show_name.like(str)) \
            .paginate(page, per_page=Config.per_page, error_out=False).items
        conn.close()
        return shows
    except:
        print('[db]: p_find_shows_by_name failed')
        return None





