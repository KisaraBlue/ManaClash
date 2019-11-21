import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from manaclash import app, db, bcrypt
from manaclash.forms import RegistrationForm, LoginForm, UpdateAccountForm
from manaclash.forms import CardForm
from manaclash.models import User, Card
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        H = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=H)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, you can log in now!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',
                                picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/cards")
def cards():
    return render_template('cards.html',
                           cards_list=Card.query.all(), title='Cards')


@app.route("/card/new", methods=['GET', 'POST'])
@login_required
def new_card():
    form = CardForm()
    if form.validate_on_submit():
        card = Card(name=form.name.data, author=current_user,
                    category=form.category.data)
        if card.category == 'Creature':
            card.creature_type = form.creature_type.data
            card.attack = form.attack.data
            card.defense = form.defense.data
        else:
            card.enchantment_type = form.enchantment_type.data
            card.effect = form.effect.data
            card.mana_cost = form.mana_cost.data
        db.session.add(card)
        db.session.commit()
        flash('Your card has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_card.html', title='New Card',
                           form=form, legend='New Card')


@app.route("/card/<int:card_id>")
def card(card_id):
    card = Card.query.get_or_404(card_id)
    return render_template('card.html', title=card.title, card=card)


@app.route("/card/<int:card_id>/update", methods=['GET', 'POST'])
@login_required
def update_card(card_id):
    card = Card.query.get_or_404(card_id)
    if card.author != current_user:
        abort(403)
    form = CardForm()
    if form.validate_on_submit():
        card.name = form.name.data
        card.category = form.category.data
        if card.category == 'Creature':
            card.creature_type = form.creature_type.data
            card.attack = form.attack.data
            card.defense = form.defense.data
            card.enchantment_type = db.NULL
            card.effect = 'No effect'
            card.mana_cost = 0
        else:
            card.enchantment_type = form.enchantment_type.data
            card.effect = form.effect.data
            card.mana_cost = form.mana_cost.data
            card.creature_type = db.NULL
            card.attack = 0
            card.defense = 0
        db.session.commit()
        flash('Your card has been updated!', 'success')
        return redirect(url_for('card', card_id=card.id))
    elif request.method == 'GET':
        form.title.data = card.title
        form.content.data = card.content
    return render_template('create_card.html', title='Update Card',
                           form=form, legend='Update Card')


@app.route("/card/<int:card_id>/delete", methods=['POST'])
@login_required
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)
    if card.author != current_user:
        abort(403)
    db.session.delete(card)
    db.session.commit()
    flash('Your card has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template('about.html', title='About')
