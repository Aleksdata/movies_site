import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from . import app, db
from .forms import ReviewForm, MovieForm, LoginForm
from .models import Movie, Review, User


UPLOAD_PATH = os.path.join(app.root_path, 'static/images/')


@app.route('/')
def index():
    movies = Movie.query.order_by(Movie.id.desc()).all()
    return render_template('index.html',
                           movies=movies)

@app.route('/movie/<int:id>', methods=['GET', 'POST'])
def movie(id):
    movie = Movie.query.get(id)
    if movie.reviews:
        avg_score = round(sum(review.score for review in movie.reviews) / len(movie.reviews), 2)
    else:
        avg_score = 0
    form = ReviewForm(score=10) ##WHATIS10
    if form.validate_on_submit():
        review = Review()
        review.name = form.name.data
        review.text = form.text.data
        review.score = form.score.data
        review.movie_id = movie.id
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('movie', id=movie.id))
    return render_template('movie.html',
                       movie=movie,
                       avg_score=avg_score,
                       form=form)


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm()
    request_data = request.data
    if form.validate_on_submit():
        movie = Movie()
        movie.title = form.title.data
        movie.description = form.description.data

        image_file = form.image.data
        filename = secure_filename(image_file.filename)
        movie.image = filename
        filepath = os.path.join(UPLOAD_PATH, filename)
        image_file.save(filepath)

        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('movie', id=movie.id))
    return render_template('add_movie.html',
                           form=form,
                           request_data=request_data)


@app.route('/reviews')
@login_required
def reviews():
    reviews = Review.query.order_by(Review.created_date.desc()).all()
    return render_template('reviews.html',
                           reviews=reviews)

@app.route('/delete_review/<int:id>')
@login_required
def delete_review(id):
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('reviews'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Вход выполнен!', 'alert-success')
            return redirect(url_for('index'))
        else:
            flash('Вход не выполнен!', 'alert-danger')
    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))