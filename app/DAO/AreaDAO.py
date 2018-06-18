from sqlalchemy import func

from app.DAO.create_schema import Area, Connection

# stadiumId = Column(Integer, ForeignKey('stadium.stadiumId'), primary_key=True)
# areaId = Column(Integer, primary_key=True)
# areaName = Column(String(20))  # 区域名
# coordinate = Column(String(30))  # 该区域在场馆底图中的位置 todo 这里先占个空，后面要改


def add_an_area(area):
    conn = Connection()
    try:
        conn.add(area)
        conn.commit()
        conn.close()
        return ('[db]:新增场馆区域成功')
    except:
        conn.rollback()
        return ('[db]:rollback add_an_area')


def delete_an_area(stadium_id, area_id):
    conn = Connection()
    try:
        area = conn.query(Area).filter_by(area_id=area_id,stadium_id=stadium_id).first()
        conn.delete(area)
        conn.commit()
        conn.close()
        return '[db]:删除区域成功'
    except:
        conn.rollback()
        return '[db]:rollback delete_an_area'


def edit_an_area(s_id,a_id,new_area):
    conn = Connection()
    try:
        area = conn.query(Area).filter_by(area_id=a_id,stadium_id=s_id).first()
        area.area_name=new_area.area_name
        area.coordinate = new_area.coordinate
        area.row_count = new_area.row_count
        area.col_count = new_area.col_count
        conn.commit()
        conn.close()
        print('[db]:编辑区域成功')
    except:
        conn.rollback()
        print('[db]:rollback edit_an_area')


def find_areas_by_stadium(stadium_id):
    conn = Connection()
    try:
        areas_in_stadium = conn.query(Area.stadium_id,Area.area_id,Area.area_name,Area.coordinate,Area.row_count,Area.col_count)\
            .filter_by(stadium_id=stadium_id)\
            .all()
        conn.close()
        return areas_in_stadium
    except:
        print('[db]:find_areas_by_stadium failed')
        return None


def get_max_area_id(stadium_id):
    conn = Connection()
    num = conn.query(func.max(Area.area_id))\
        .filter_by(stadium_id=stadium_id)\
        .first()
    conn.close()
    return num





