from flask import request
from sqlalchemy.ext.declarative import declarative_base
from math import ceil
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship, mapper, Query
from werkzeug.exceptions import abort

from config import Config

__author__ = 'yummysghhz'

Base = declarative_base()
engine = create_engine(Config.my_db_conn)
Connection = sessionmaker(bind=engine, expire_on_commit=False)

# 改动
# 需要show_id, session_id来做联合主键的地方全都改成price_id了
# artist里加了艺人图片
# stadium里加了city
# shows里面加了show_pic（演出海报地址）
# area里加了row_count, col_count
# 去掉了show_session的end_time（演出结束时间）
# 加了个price_with_session表
# 票价类型改成了numeric/decimal型
# 无座订单详情里加了price_id项（e.g. 考虑某活动：一人票80，两人票150）
# 改了若干表的组合外键约束

# todo 座位里description要包含楼层信息
# todo 考虑订单里加入座位详细信息描述（以防之后座位被改掉？）憋了。。。还是别那么复杂吧。。。

# todo 考虑做个缺货登记表、站内信表


# 艺人
class Artist(Base):
    __tablename__ = 'artist'

    artist_id = Column(Integer, primary_key=True, autoincrement=True)
    artist_name = Column(String(20), nullable=False)
    artist_pic = Column(String(20))


# 关注（艺人）
class Follows(Base):
    __tablename__ = 'follows'

    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artist.artist_id'), primary_key=True)


# 演出-艺人对应表
class Includes(Base):
    __tablename__ = 'includes'

    show_id = Column(Integer, ForeignKey('shows.show_id'), primary_key=True)
    artist = Column(Integer, ForeignKey('artist.artist_id'), primary_key=True)


# 用户
class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)
    tel = Column(String(15))
    role = Column(String(20), nullable=False, default='普通用户')  # todo 没有键emmmm......
    id_card = Column(String(20))  # 身份证号 todo 购票时不能为空


# 权限
class Authority(Base):
    __tablename__ = 'authority'

    role = Column(String(20), primary_key=True)

    # 就是某角色可以有的操作，想叫权限的可都叫authority不好吧？？？
    permission = Column(String(30), primary_key=True)  # todo user表里的role和这里的role都没有单独成键，肿么办？？？


# 场馆
class Stadium(Base):
    __tablename__ = 'stadium'

    stadium_id = Column(Integer, primary_key=True, autoincrement=True)
    stadium_name = Column(String(20), nullable=False)
    address = Column(String(50), nullable=False)
    city = Column(String(6))
    has_seats = Column(Boolean, default=False)  # 有无座位，设置演出时需要确认座位情况
    pic_src = Column(String(20))  # 场馆底图（包含了很多可选区域的大致图），可以为空

    areas = relationship('Area', backref='its_stadium')


# 场馆里的区域（差不多是分割场馆的块吧）
class Area(Base):
    __tablename__ = 'area'

    stadium_id = Column(Integer, ForeignKey('stadium.stadium_id'), primary_key=True)
    area_id = Column(Integer, primary_key=True)
    area_name = Column(String(20))  # 区域名
    coordinate = Column(String(30))  # 该区域在场馆底图中的位置 todo 这里先占个空，后面要改
    row_count = Column(Integer)
    col_count = Column(Integer)

    # leftTopX = Column(Integer)  # 这里后面要改的！目前做法：先把场馆底图分割成若干矩形区域，记录左上角和右下角坐标
    # leftTopY = Column(Integer)  # 同上
    # rightBottomX = Column(Integer)  # 同上
    # rightBottomY = Column(Integer)  # 同上

    # seats = relationship('Seat', backref='its_area')


# 座位
seat = Table('seat', Base.metadata,
             Column('seat_id', Integer, primary_key=True, autoincrement=True),
             Column('x', Integer),  # 二维矩阵（座位图）中x
             Column('y', Integer),  # 二维矩阵（座位图）中y
             Column('row_no', Integer),  # 实际位置：几排
             Column('seat_no', Integer),  # 实际位置：几座
             Column('description', String(20)),  # 比如可以区分更小的块：一号桌，块五等等
             Column('stadium_id', Integer),
             Column('area_id', Integer),
             ForeignKeyConstraint(('stadium_id', 'area_id'), ('area.stadium_id', 'area.area_id'))
             )


class Seat(object):
    def __init__(self, seat_id=None, x=None, y=None, row_no=None, seat_no=None, description=None, stadium_id=None,
                 area_id=None
                 ):
        self.seat_id = seat_id
        self.x = x
        self.y = y
        self.row_no = row_no
        self.seat_no = seat_no
        self.description = description
        self.stadium_id = stadium_id
        self.area_id = area_id


mapper(Seat, seat)


# # 座位
# class Seat(Base):
#     __tablename__ = 'seat'
#
#     seat_id = Column(Integer, primary_key=True, autoincrement=True)
#     x = Column(Integer)  # 二维矩阵（座位图）中x
#     y = Column(Integer)  # 二维矩阵（座位图）中y
#     row_no = Column(Integer)  # 实际位置：几排
#     seat_no = Column(Integer)  # 实际位置：几座
#     description = Column(String(20))  # 比如可以区分更小的块：一号桌，块五等等
#     stadium_id = Column(Integer)
#     area_id = Column(Integer)
#     ForeignKeyConstraint(('stadium_id', 'area_id'), ('area.stadium_id', 'area.area_id'))


# 演出
class Shows(Base):
    __tablename__ = 'shows'

    show_id = Column(Integer, primary_key=True, autoincrement=True)
    show_name = Column(String(50), nullable=False)
    show_type = Column(Integer, nullable=False)
    show_pic = Column(String(30))
    description_file = Column(String(20))  # todo 描述文件，后期可能就把它做成一个description了？然而描述内容好多啊_(:3
    stadium_id = Column(Integer, ForeignKey('stadium.stadium_id'))
    can_choose_seats = Column(Boolean)  # 是否可以选座
    producer = Column(String(30))  # 制作方


# 场次
class ShowSession(Base):
    __tablename__ = 'show_session'

    show_id = Column(Integer, ForeignKey('shows.show_id'), primary_key=True)
    session_id = Column(Integer, primary_key=True)
    start_time = Column(DATETIME)  # 演出开始时间
    sale_time = Column(DATETIME)  # 开售时间
    end_sale_time = Column(DATETIME)  # 售票结束时间
    limit = Column(Integer)  # todo 单人购票上限，考虑移到别处（如果做团队购票/分销的话）


# # 票价类型/票种
# class TicketPrice(Base):
#     __tablename__ = 'ticket_price'
#
#     price_id = Column(Integer, primary_key=True, autoincrement=True)
#     # type = Column(String(1), primary_key=True),  # 'a', 'b', ...
#     price = Column(Numeric(8, 2), nullable=True)
#     description = Column(String(10))  # 'a级座位' 什么的。。。或者考虑这里换成a,b,c,...?
#     color = Column(String(10))  # 显示颜色，表达成 '[#]ffee33' 这种的


# 票价类型/票种-场次对应表
price_with_session = Table('price_with_session', Base.metadata,
                           Column('show_id', Integer, primary_key=True),
                           Column('session_id', Integer, primary_key=True),
                           Column('price_id', Integer, primary_key=True),
                           Column('price', Numeric(8, 2), nullable=True),
                           Column('t_desc', String(10)),
                           Column('color', String(10)),
                           ForeignKeyConstraint(('show_id', 'session_id'),
                                                ('show_session.show_id', 'show_session.session_id'))
                           )


# 票价类型/票种
class PriceWithSession(object):
    def __init__(self, show_id=None, session_id=None, price_id=None, price=None, t_desc=None, color=None):
        self.show_id = show_id
        self.session_id = session_id
        self.price_id = price_id
        self.price = price
        self.t_desc = t_desc
        self.color = color


mapper(PriceWithSession, price_with_session)

# # 场次与价位的关联表
# price_with_session = Table('price_with_session', Base.metadata,
#                            Column('show_id', Integer, primary_key=True),
#                            Column('session_id', Integer, primary_key=True),
#                            Column('price_id', ForeignKey('ticket_price.price_id'), primary_key=True),
#                            ForeignKeyConstraint(('show_id', 'session_id'),
#                                                 ('show_session.show_id', 'show_session.session_id'))
#                            )
#
#
# class PriceWithSession(object):
#     def __init__(self, show_id=None, session_id=None, price_id=None):
#         self.show_id = show_id
#         self.session_id = session_id
#         self.price_id = price_id


# mapper(PriceWithSession, price_with_session)

# 每个演出场次每个座位的状态
# todo 在往这张表里插入的时候，要先检查座位在不在这个场馆里
seat_status = Table('seat_status', Base.metadata,
                    Column('show_id', Integer, primary_key=True),
                    Column('session_id', Integer, primary_key=True),
                    Column('seat_id', Integer, ForeignKey('seat.seat_id'), primary_key=True),
                    Column('price_id', Integer),
                    Column('status', String(20), default='available'),
                    # todo 之后会改成【Enum】类型，加个default='available'？还是用数字来表示状态？
                    ForeignKeyConstraint(('show_id', 'session_id', 'price_id'),
                                         ('price_with_session.show_id', 'price_with_session.session_id',
                                          'price_with_session.price_id'))
                    )


class SeatStatus(object):
    def __init__(self, show_id=None, session_id=None, seat_id=None, price_id=None, status=None):
        self.show_id = show_id
        self.session_id = session_id
        self.seat_id = seat_id
        self.price_id = price_id
        self.status = status


mapper(SeatStatus, seat_status)

# 每个无座演出的票数现状
ticket_with_no_seat = Table('ticket_with_no_seat', Base.metadata,
                            Column('show_id', Integer, primary_key=True),
                            Column('session_id', Integer, primary_key=True),
                            Column('price_id', Integer, primary_key=True),
                            Column('remaining_count', Integer),  # 剩余票数
                            ForeignKeyConstraint(('show_id', 'session_id', 'price_id'),
                                                 ('price_with_session.show_id', 'price_with_session.session_id',
                                                  'price_with_session.price_id'))
                            )


class TicketWithNoSeat(object):
    def __init__(self, show_id=None, session_id=None, price_id=None, remaining_count=None):
        self.show_id = show_id
        self.session_id = session_id
        self.price_id = price_id
        self.remaining_count = remaining_count


mapper(TicketWithNoSeat, ticket_with_no_seat)


# 订单
class UserOrder(Base):
    __tablename__ = 'user_order'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    with_seats = Column(Boolean)  # todo 是否有座，指示查看订单详情的时候去哪张表查
    total_price = Column(Numeric(10, 2))
    order_time = Column(DATETIME)
    pay_time = Column(DATETIME)
    order_status = Column(String(10), default='未付款')  # todo 之后会改成【Enum】类型，加个default='未付款'？还是用数字表示？
    # seats = relationship('Seat', backref='its_order') 要做，待测


# 有座订单详情
order_details_with_seats = Table('order_details_with_seats', Base.metadata,
                                 Column('order_id', Integer, ForeignKey('user_order.order_id'), primary_key=True),
                                 Column('show_id', Integer, primary_key=True),
                                 Column('session_id', Integer, primary_key=True),
                                 Column('seat_id', Integer, primary_key=True),
                                 Column('price', Numeric(8, 2)),  # 价格可能变动
                                 ForeignKeyConstraint(('show_id', 'session_id', 'seat_id'),
                                                      ('seat_status.show_id', 'seat_status.session_id',
                                                       'seat_status.seat_id'))
                                 )


class OrderDetailsWithSeat(object):
    def __init__(self, order_id=None, show_id=None, session_id=None, seat_id=None, price=None):
        self.order_id = order_id
        self.show_id = show_id
        self.session_id = session_id
        self.seat_id = seat_id
        self.price = price


mapper(OrderDetailsWithSeat, order_details_with_seats)

# 无座订单详情
order_details_with_no_seat = Table('order_details_with_no_seat', Base.metadata,
                                   Column('order_id', Integer, ForeignKey('user_order.order_id'), primary_key=True),
                                   Column('show_id', Integer, primary_key=True),
                                   Column('session_id', Integer, primary_key=True),
                                   Column('price_id', Integer, primary_key=True),
                                   Column('price', Numeric(8, 2), nullable=True),  # 价格可能变动
                                   Column('ticket_count', Integer, nullable=True),
                                   ForeignKeyConstraint(('show_id', 'session_id', 'price_id'),
                                                        (
                                                            'ticket_with_no_seat.show_id',
                                                            'ticket_with_no_seat.session_id',
                                                            'ticket_with_no_seat.price_id'))
                                   )


class OrderDetailsWithNoSeat(object):
    def __init__(self, order_id=None, show_id=None, session_id=None, price_id=None, price=None, ticket_count=None):
        self.order_id = order_id
        self.show_id = show_id
        self.session_id = session_id
        self.price_id = price_id
        self.price = price
        self.ticket_count = ticket_count


mapper(OrderDetailsWithNoSeat, order_details_with_no_seat)


def create():
    Base.metadata.create_all(engine)


class Pagination(object):
    """
    分页对象
    """
    def __init__(self, query, page, per_page, total, items):
        self.query = query
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items

    @property
    def pages(self):
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def prev(self, error_out=False):
        assert self.query is not None, 'a query object is required ' \
                                       'for this method to work'
        return self.query.paginate(self.page - 1, self.per_page, error_out)

    @property
    def prev_num(self):
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def has_prev(self):
        return self.page > 1

    def next(self, error_out=False):
        assert self.query is not None, 'a query object is required ' \
                                       'for this method to work'
        return self.query.paginate(self.page + 1, self.per_page, error_out)

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(self):
        if not self.has_next:
            return None
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (self.page - left_current - 1 < num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


def paginate(self, page=None, per_page=None, error_out=True):
    """
    分页函数
    :param self:
    :param page:
    :param per_page:
    :param error_out:
    :return:
    """
    if request:
        if page is None:
            try:
                page = int(request.args.get('page', 1))
            except (TypeError, ValueError):
                if error_out:
                    abort(404)

                page = 1

        if per_page is None:
            try:
                per_page = int(request.args.get('per_page', 20))
            except (TypeError, ValueError):
                if error_out:
                    abort(404)

                per_page = 20
    else:
        if page is None:
            page = 1

        if per_page is None:
            per_page = 20

    if error_out and page < 1:
        abort(404)

    items = self.limit(per_page).offset((page - 1) * per_page).all()

    if not items and page != 1 and error_out:
        abort(404)

    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = self.order_by(None).count()

    return Pagination(self, page, per_page, total, items)


# 在原查询类上加上分页方法
Query.paginate = paginate
create()
