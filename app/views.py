"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from app import app, db, login_manager
from flask import render_template, flash, send_from_directory, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, PropertyForm
from app.models import UserProfile, Property
from werkzeug.utils import secure_filename
import os


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Daniel Graham")


@app.route('/properties/create', methods=['GET', 'POST'])
@login_required
def create_property():
    form = PropertyForm()

    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(upload_path)

        property = Property(
            title=form.title.data,
            description=form.description.data,
            bedrooms=form.bedrooms.data,
            bathrooms=form.bathrooms.data,
            location=form.location.data,
            price=form.price.data,
            property_type=form.property_type.data,
            photo_filename=filename,
            user_id=current_user.id
        )

        db.session.add(property)
        db.session.commit()

        flash('Property successfully added!', 'success')
        return redirect(url_for('properties'))

    return render_template('create_property.html', form=form)

@app.route('/properties')
def properties():
    """Display a list of all properties."""
    properties_list = Property.query.all()
    return render_template('properties.html', properties=properties_list)


@app.route('/properties/<int:property_id>')
def view_property(property_id):
    """Display an individual property by ID."""
    this_property = Property.query.get_or_404(property_id)
    return render_template('view_property.html', property=this_property)


@app.route('/uploads/<filename>')
def get_image(filename):
    """Return an image from the uploads folder."""
    upload_folder = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
    return send_from_directory(upload_folder, filename)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('properties'))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserProfile.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Successfully logged in!', 'success')
            return redirect(url_for('properties'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('login'))

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


