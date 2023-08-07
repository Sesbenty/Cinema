from app_config import db


class CinemaSession(db.Model):
    __tablename__ = 'cinema_session'
    id = db.Column('id', db.INTEGER, primary_key=True, autoincrement=True)
    session_date = db.Column('session_date', db.DateTime, nullable=False)
    hall_id = db.Column('hall_id', db.ForeignKey('hall.id'))
    movie_id = db.Column('movie_id', db.ForeignKey('movie.id'))


class Hall(db.Model):
    __tablename__ = 'hall'
    id = db.Column('id', db.INTEGER, primary_key=True, autoincrement=True)
    hall_name = db.Column('hall_name', db.String(30), nullable=False)
    number_place = db.Column('number_place', db.INTEGER, nullable=False)
    number_row = db.Column('number_row', db.INTEGER, nullable=False)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column('id', db.INTEGER, primary_key=True, autoincrement=True)
    movie_name = db.Column('movie_name', db.String(30), nullable=False)
    movie_time = db.Column('movie_time', db.DateTime, nullable=False)


class Site(db.Model):
    __tablename__ = 'site'
    id = db.Column('id', db.INTEGER, primary_key=True, autoincrement=True)
    site_place = db.Column('site_place', db.INTEGER, nullable=False)
    site_row = db.Column('site_row', db.INTEGER, nullable=False)
    hall_id = db.Column('hall_id', db.ForeignKey('hall.id'), nullable=False, )


class Ticket(db.Model):
    __tablename__ = 'Ticket'
    id = db.Column('id', db.INTEGER, primary_key=True, autoincrement=True)
    ticket_price = db.Column('ticket_price', db.DateTime, nullable=False)
    session_id = db.Column('session_id', db.ForeignKey('cinema_session.id'), nullable=False)
    site_id = db.Column('site_id', db.ForeignKey('site.id'), nullable=False)