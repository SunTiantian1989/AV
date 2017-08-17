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


class Cast(db.Model):
    __tablename__='casts'
    id = db.Column(db.Integer, primary_key=True)
    cast_name = db.Column(db.String, nullable=False, unique=True)


class Genre(db.Model):
    __tablename__='genres'
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String, nullable=False, unique=True)


class CastInVideo:
    __tablename__ = 'casts_in_videos'
    id = db.Column(db.Integer, primary_key=True)
    video_number = db.Column(db.String, nullable=False)
    cast_name = db.Column(db.String, nullable=False, unique=True)


class GenreInVideo:
    __tablename__ = 'genres_in_videos'
    id = db.Column(db.Integer, primary_key=True)
    video_number = db.Column(db.String, nullable=False)
    genre_name = db.Column(db.String, nullable=False, unique=True)
