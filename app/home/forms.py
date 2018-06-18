from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class SearchForm(FlaskForm):
    city = StringField(label='城市')
    stadium = StringField(label='场馆')
    artist = StringField(label='艺人')
    show_title = StringField(label='演出')


class LoginForm(FlaskForm):
    username = StringField(label='用户名',
                           validators=[DataRequired('用户名不能为空'), Length(1, 20, '长度不超过20')],
                           render_kw={'placeholder': '20字以内', 'class': 'form-control'})
    password = PasswordField(label='密码',
                             validators =[DataRequired('密码不能为空'), Length(1, 20, '长度不超过20')],
                             render_kw={'placeholder': '20字以内','class': 'form-control'}
                             )
    submit = SubmitField('登录',
                         render_kw={'class': 'form-control'})


class RegisterForm(FlaskForm):
    username = StringField(label='用户名',
                           validators=[DataRequired('用户名不能为空'), Length(1, 20, '长度不超过20')],
                           render_kw={'placeholder': '20字以内','class':'form-control'}
                           )
    password = PasswordField(label='密码',
                             validators=[DataRequired('密码不能为空'), Length(1, 20, '长度不超过20')],
                             render_kw={'placeholder': '20字以内','class': 'form-control'}
                             )
    password2 = PasswordField(label='重复密码',
                              validators=[
                                  DataRequired('密码不能为空'),
                                  EqualTo('password','两次输入不一致')],
                              render_kw={'placeholder': '20字以内', 'class': 'form-control'}
                              )
    tel = StringField(label='联系电话',
                      validators=[Length(7, 15,'长度不超过15')],
                      render_kw={'id': 'tel', 'placeholder': '15字以内', 'class': 'form-control'}
                      )
    idCard = StringField(label='身份证号',
                         validators=[Length(12, 20,'长度不超过20')],
                         render_kw={'placeholder': '20字以内','class': 'form-control'}
                         )
    submit = SubmitField('注册',
                         render_kw={'class': 'form-control'})



