from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField, DateTimeField, IntegerField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length
from app import stadiumImgs, showImgs, showDescFiles, artistImgs


class StadiumForm(FlaskForm):
    stadiumId = IntegerField(label='场馆id')
    stadiumName = StringField(label='场馆名称',
                              validators=[DataRequired('场馆名不能为空'), Length(1, 10, '长度不超过10')],
                              render_kw={'placeholder': '10字以内', 'class': 'form-control'})
    city = StringField(label='所在城市',
                       validators=[DataRequired('必选')],
                       render_kw={'placeholder': '10字以内', 'class': 'form-control'})
    address = StringField(label='地址',
                          validators=[DataRequired('地址不能为空'), Length(1, 25, '长度不超过25')],
                          render_kw={'placeholder': '25字以内', 'class': 'form-control'})
    hasSeats = BooleanField(label='可选座',
                            default=False)
    picSrc = FileField('示意图',
                       validators=[FileAllowed(stadiumImgs, '仅允许上传图片(<1MB)!')],
                       render_kw={'class': 'form-control'})
    submit = SubmitField('提交',
                         render_kw={'class': 'form-control'})


class ShowForm(FlaskForm):
    showId = IntegerField(label='演出id')
    showName = StringField(label='演出名称',
                           validators=[DataRequired('不能为空'), Length(1, 50, '长度不超过50')],
                           render_kw={'placeholder': '50字以内', 'class': 'form-control'})
    showType = SelectField(label='类型', coerce=int,
                           validators=[DataRequired('不能为空')],
                           choices=[(1, '演唱会'),(2,'话剧'),(3,'小型现场')])
    producer = StringField(label='制作方',
                           render_kw={'placeholder': '50字以内', 'class': 'form-control'})
    showPic = FileField(label='海报',
                        validators=[FileAllowed(showImgs, '仅允许上传图片(<1MB)!')],
                        render_kw={'class': 'form-control'})
    descriptionFile = FileField(label='简介',
                                validators=[FileAllowed(showDescFiles, '上传文字描述(<1MB)!')],
                                render_kw={'class': 'form-control'})
    stadiumId = SelectField(coerce=int, label='场馆', validators=None)
    canChooseSeats = BooleanField('可选座', default=False)
    submit = SubmitField('确定',
                         render_kw={'class': 'form-control'})


class SessionForm(FlaskForm):
    show_id=IntegerField('演出id')
    session_id=IntegerField('场次id')
    start_time = DateTimeField(label='开演',
                               render_kw={'placeholder': 'format:%Y-%m-%d %H:%M:%S', 'class': 'form-control'})
    sale_time = DateTimeField('开始售票',
                              render_kw={'placeholder': 'format:%Y-%m-%d %H:%M:%S', 'class': 'form-control'})
    end_sale_time = DateTimeField('停止售票',
                                  render_kw={'placeholder': 'format:%Y-%m-%d %H:%M:%S', 'class': 'form-control'})
    limit = IntegerField('单笔上限数')
    submit = SubmitField('提交')


class ArtistForm(FlaskForm):
    artist_id = StringField(label='艺人id')
    artist_name = StringField(label='艺人/团体',
                              validators=[DataRequired('不能为空'), Length(1, 20, '长度不超过20')],
                              render_kw={'placeholder': '20字以内', 'class': 'form-control'})
    artist_pic = FileField(label='照片',
                        validators=[FileAllowed(artistImgs, '仅允许上传图片(<1MB)!')],
                        render_kw={'class': 'form-control'})
    submit = SubmitField('提交')


class AreaForm(FlaskForm):
    # todo id-readonly 行列的大小范围？？
    # coordinate是框选得到的矩形区左上xy与右下xy，多个字段or带分隔符的一个字段？？
    stadium_id = IntegerField(label='场馆id')
    area_id = IntegerField(label='区域id')
    area_name = StringField(label='区域名称',
                            validators=[DataRequired('不能为空'), Length(1, 20, '长度不超过20')],
                            render_kw={'placeholder': '20字以内', 'class': 'form-control'})
    # coordinate = StringField(label='区域界定')
    x1 = IntegerField(label='x1',
                      validators=[DataRequired('不能为空')])
    y1 = IntegerField(label='y1',
                      validators=[DataRequired('不能为空')])
    x2 = IntegerField(label='x2',
                      validators=[DataRequired('不能为空')])
    y2 = IntegerField(label='y2',
                      validators=[DataRequired('不能为空')])
    row_count = IntegerField(label='行数',
                             validators=[DataRequired('不能为空')])
    col_count = IntegerField(label='列数',
                             validators=[DataRequired('不能为空')])
    submit = SubmitField('提交')
