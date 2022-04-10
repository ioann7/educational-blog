from wtforms import StringField, TextAreaField, ValidationError
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from app.models import Post, slugify


class PostForm(FlaskForm):
    title = StringField('Title', validators=(DataRequired(),))
    body = TextAreaField('Body', validators=(DataRequired(),))

    def validate_title(self, title):
        slug = Post.query.filter_by(slug=slugify(title.data)).first()
        if slug is not None:
            raise ValidationError('Please use different titles')
