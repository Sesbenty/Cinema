from app_config import app, db
from model import *

from sqlalchemy import literal
from flask import request, render_template, redirect, url_for
from sqlalchemy import desc

#from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from app_config import db;

@app.route("/movie/<int:id>")
def movie(id):
    movie = db.session.query(Movie).filter(Movie.id == id).one_or_none()
    if movie is None:
        return 'Not Found', 404

    return render_template(
        "movie.html",
        movie=movie
    )


@app.route("/movie", methods=['GET', 'POST'])
def list_movie():
    n = db.session.query(Movie). \
        all()
    movie_name =''
    if request.method == 'POST':
        movie_name = request.form['search']
        l=list()
        for s in n:
            if movie_name.lower() in s.movie_name.lower():
                l.append(s)
        n = l
    return render_template("movie_list.html", movies=n, name=movie_name)


@app.route("/session/<int:id>")
def cinema_session(id):
    session = db.session.query(CinemaSession).filter(CinemaSession.id == id).one_or_none()
    if session is None:
        return 'Not Found', 404

    movie = db.session.query(Movie).filter(Movie.id == session.movie_id).one_or_none()
    hall = db.session.query(Hall).filter(Hall.id == session.hall_id).one_or_none()
    tickets = db.session.query(Ticket).filter(Ticket.session_id == session.id).all()
    return render_template("cinema_session.html", cinema_session=session, movie=movie, hall=hall, tickets=tickets)

@app.route('/', methods=['GET', 'POST'])
@app.route("/session", methods=['GET', 'POST'])
def list_cinema_session():
    sessions = db.session.query(CinemaSession, Movie).filter(CinemaSession.movie_id == Movie.id).all()
    if request.method == 'POST':
        movie_name = request.form['search']
        l = list()
        for i in sessions:
            if movie_name.lower() in i[1].movie_name.lower():
                l.append(i)
        sessions = l
    s = [{"cinema_session": i[0], "movie": i[1]} for i in sessions]
    return render_template("cinema_session_list.html", session_movie_list=s)


@app.route("/movie_edit/<int:id>", methods=['GET', 'POST'])
def edit_movie(id):
    if id == 0:
        movie = Movie()
    else:
        movie = db.session.query(Movie).filter(Movie.id == id).one_or_none()
        if movie is None:
            return 'Not Found', 404

    if request.method == 'POST':
        if request.form['command'] == "Сохранить":
            movie.movie_name = request.form['name']
            movie.movie_time = request.form['time']
            try:
                db.session.add(movie)
                db.session.commit()
                if id == 0:
                    db.session.flush()
                    return redirect(url_for('edit_movie', id=movie.id))
            except:
                return "Ошибка"
        if request.form['command'] == 'Удалить':
            sessions = db.session.query(CinemaSession).filter(CinemaSession.movie_id == movie.id)
            for session in sessions:
                db.session.query(Ticket).filter(Ticket.session_id == session.id).delete()
                db.session.delete(session)
            db.session.delete(movie)
            db.session.commit()
            return redirect('/')
    return render_template("movie_edit.html", movie=movie)


@app.route("/session_edit/<int:id>", methods=['GET', 'POST'])
def edit_session(id):
    movies = db.session.query(Movie).all()
    halls = db.session.query(Hall).all()
    if id == 0:
        session = CinemaSession()
    else:
        session = db.session.query(CinemaSession).filter(CinemaSession.id == id).one_or_none()
        if session is None:
            return 'Not Found', 404

    if request.method == 'POST':
        if request.form['command'] == "Сохранить":
            session.session_date = request.form['date']
            session.movie_id = request.form['movie_id']
            session.hall_id = request.form['hall_id']
            price = request.form['price']
            try:
                db.session.add(session)
                db.session.commit()
                if id == 0:
                    hall = db.session.query(Hall).filter(Hall.id == session.hall_id).one_or_none()
                    sites = db.session.query(Site).filter(Site.hall_id == hall.id)
                    for site in sites:
                        ticket = Ticket()
                        ticket.session_id = session.id
                        ticket.ticket_price = price
                        ticket.site_id = site.id
                        db.session.add(ticket)
                    db.session.commit()
                    db.session.flush()
                    return redirect(url_for('edit_session', id=session.id))
                else:
                    db.session.query(Ticket).filter(Ticket.session_id == session.id).delete()
                    sites = db.session.query(Site).filter(Site.hall_id == session.hall_id)
                    for site in sites:
                        ticket = Ticket()
                        ticket.session_id = session.id
                        ticket.ticket_price = int(price)
                        ticket.site_id = site.id
                        db.session.add(ticket)
                    db.session.commit()
                    return redirect(url_for('edit_session', id=session.id))
            except:
                return "Ошибка"
        if request.form['command'] == 'Удалить':
            db.session.query(Ticket).filter(Ticket.session_id == session.id).delete()
            db.session.delete(session)
            db.session.commit()
            return redirect('/')
        if request.form['command']:
            session.movie_id = request.form['movie_id']
    movie = db.session.query(Movie).filter(Movie.id == session.movie_id).one_or_none()
    hall = db.session.query(Hall).filter(Hall.id == session.hall_id).one_or_none()
    tickets = db.session.query(Ticket).filter(Ticket.session_id == session.id).all()
    price = 0
    if len(tickets) > 0:
        price = tickets[0].ticket_price

    return render_template("cinema_session_edit.html", session=session, movies=movies, movie=movie, halls=halls, hall=hall, price=price)


@app.route("/hall_edit/<int:id>", methods=['GET', 'POST'])
def edit_hall(id):
    if id == 0:
        hall = Hall()
    else:
        hall = db.session.query(Hall).filter(Hall.id == id).one_or_none()
        if hall is None:
            return 'Not Found', 404

    if request.method == 'POST':
        if request.form['command'] == "Сохранить":
            hall.hall_name = request.form['name']
            hall.number_row = request.form['row']
            hall.number_place = request.form['place']
            try:
                db.session.add(hall)
                db.session.commit()
                if id == 0:
                    for x in range(1, int(hall.number_place) + 1):
                        for y in range(1, int(hall.number_row) + 1):
                            site = Site()
                            site.hall_id = int(hall.id)
                            site.site_place = x;
                            site.site_row = y;
                            db.session.add(site)
                    db.session.commit()
                    db.session.flush()
                    return redirect(url_for('edit_hall', id=hall.id))
                else:
                    sessions = db.session.query(CinemaSession).filter(CinemaSession.hall_id == hall.id)
                    for session in sessions:
                        db.session.query(Ticket).filter(Ticket.session_id == session.id).delete()
                        db.session.delete(session)
                    for x in range(1, int(hall.number_place) + 1):
                        for y in range(1, int(hall.number_row) + 1):
                            site = Site()
                            site.hall_id = int(hall.id)
                            site.site_place = x;
                            site.site_row = y;
                            db.session.add(site)
                    db.session.commit()
            except:
                return "Ошибка"
        if request.form['command'] == 'Удалить':
            sessions = db.session.query(CinemaSession).filter(CinemaSession.hall_id == hall.id)
            for session in sessions:
                db.session.query(Ticket).filter(Ticket.session_id == session.id).delete()
                db.session.delete(session)
            db.session.query(Site).filter(Site.hall_id == hall.id).delete()
            db.session.delete(hall)
            db.session.commit()
            return redirect('/')
    return render_template('hall_edit.html', hall=hall)


@app.route("/hall", methods=['GET', 'POST'])
def list_hall():
    halls = db.session.query(Hall). \
        all()
    return render_template("hall_list.html", halls=halls)


if __name__ == '__main__':
    # Create scheme if not exists
    db.create_all()
    app.run(host='0.0.0.0', port='80', debug=True)