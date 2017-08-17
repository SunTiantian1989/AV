from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField,SubmitField,SelectMultipleField,SelectField
from wtforms.validators import DataRequired
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY']='suntiantain'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'AV.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class Video(db.Model):
    __tablename__='videos'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=True)
    date = db.Column(db.Date, nullable=True)
    length = db.Column(db.Integer, nullable=True)
    director = db.Column(db.String, nullable=True)
    maker = db.Column(db.String, nullable=True)
    label = db.Column(db.String, nullable=True)
    review_point = db.Column(db.Integer, nullable=True)
    codec_tag = db.Column(db.String, nullable=True)
    height = db.Column(db.String, nullable=True)
    width = db.Column(db.String, nullable=True)
    bit_rate = db.Column(db.String, nullable=True)
    size = db.Column(db.String, nullable=True)


class Cast(db.Model):
    __tablename__='casts'
    id = db.Column(db.Integer, primary_key=True)
    cast_name = db.Column(db.String, nullable=False, unique=True)


class Genre(db.Model):
    __tablename__='genres'
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String, nullable=False, unique=True)


class CastInVideo(db.Model):
    __tablename__ = 'casts_in_videos'
    id = db.Column(db.Integer, primary_key=True)
    video_number = db.Column(db.String, nullable=False)
    cast_name = db.Column(db.String, nullable=False, unique=True)


class GenreInVideo(db.Model):
    __tablename__ = 'genres_in_videos'
    id = db.Column(db.Integer, primary_key=True)
    video_number = db.Column(db.String, nullable=False)
    genre_name = db.Column(db.String, nullable=False, unique=True)

all_casts = Cast.query.order_by(Cast.cast_name).all()
cast_choices = [(0,'所有')]
for cast in all_casts:
    cast_choices.append((cast.id,cast.cast_name))


class NameForm(Form):
    select=SelectField('女优', choices = cast_choices,)
    submit=SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    videos_results = []
    if form.is_submitted():
        old_name = session.get('cast_name')
        cast_id = form.select.data
        if cast_id is '0':
            videos_results = Video.query.all()
            cast_name='所有演员'
        else:
            cast_name= Cast.query.filter_by(id = cast_id).first().cast_name
            videos_numbers=CastInVideo.query.filter_by(cast_name = cast_name).order_by(CastInVideo.video_number).all()
            for videos_number in videos_numbers:
                videos_results.append(Video.query.filter_by(number = videos_number.video_number).first())
        if old_name is not None and old_name != cast_name:
            flash('换了一个！')
        session['cast_name'] = cast_name
    return render_template('index.html',
                           form=form,
                           name=session.get('cast_name'),
                           videos_results=videos_results)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



@app.route('/cookie_re/')
def cookie_re():
    response=make_response('<h1>cookie已启用</h1>')
    response.set_cookie('answer','42')
    return response


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/res')
def res():
    return redirect('/cookie_re/')


if __name__ == '__main__':
#    print(app.url_map)
    app.run(debug=True)

