from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    # 定义邮箱字段：必填+符合邮箱格式
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    # 定义密码字段：必填+长度至少为6位
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    # 定义“记住我”复选框字段
    remember_me = BooleanField('记住我')
    # 定义提交按钮
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    # 定义用户名字段：必填+长度在3-20个字符之间
    username = StringField('用户名', validators=[DataRequired(), Length(min=3, max=20)])
    # 定义邮箱字段：必填+符合邮箱格式
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    # 定义密码字段：必填+长度至少为6位
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    # 定义确认密码字段：必填+需和密码字段的值完全一致
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    # 定义提交按钮
    submit = SubmitField('注册')

    # 自定义验证器：校验用户名是否已被注册
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被注册，请选择其他用户名')

    # 自定义验证器：校验邮箱是否已被注册
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('该邮箱已被注册，请使用其他邮箱')