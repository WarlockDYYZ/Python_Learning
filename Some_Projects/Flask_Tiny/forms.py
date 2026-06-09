from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
    """登录表单类"""
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    """注册表单类"""
    username = StringField('用户名', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        """自定义验证器：校验用户名是否已被注册"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被注册，请选择其他用户名')

    def validate_email(self, email):
        """自定义验证器：校验邮箱是否已被注册"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('该邮箱已被注册，请使用其他邮箱')

class UploadForm(FlaskForm):
    """文件上传表单类"""
    file = FileField('选择文件', validators=[
        FileRequired(),
        FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'], '仅允许上传图片、PDF、文本文件')
    ])
    submit = SubmitField('上传文件')