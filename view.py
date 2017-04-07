from flask import render_template, request, redirect, flash
from app import app, env
from environment import parse_dates, parse_time_ranges, parse_time


@app.route('/')
def index():
    return redirect('/sign_up')


@app.route('/success')
def success():
    return render_template('/index_login.html')


@app.route('/sign_up', methods=('GET', 'POST'))
def sign_up():
    if request.method == 'POST':
        user = request.form.get('login', '')
        if not user:
            flash('Enter login to sign in', category='danger')
        else:
            env.add_user(user)
            return redirect('/appointment_creation')
    return render_template('login.html')


@app.route('/appointment_creation', methods=('GET', 'POST'))
def add_appointment():
    time_ranges = [(t, t + 1) for t in range(20) if 8 <= t <= 20]
    form_data = {'subject': '', 'description': '', 'additional_info': ''}
    if request.method == 'POST':
        subject = request.form.get('subject', '')
        description = request.form.get('description', '')
        additional_info = request.form.get('additional_info', '')
        initial_dates = request.form.get('selected_date')
        initial_time = request.form.getlist('selected_time')

        form_data['subject'] = subject
        form_data['description'] = description
        form_data['additional_info'] = additional_info

        if not subject:
            flash('Appointment should have subject', category='danger')
        elif not initial_dates or not initial_time:
            flash('Certain date and time are necessary', category='danger')
        else:
            parsed_dates = parse_dates(initial_dates)
            parsed_time = parse_time_ranges(initial_time)
            form_data['dates'] = parsed_dates
            form_data['time'] = parsed_time

            appointment = env.create_appointment(**form_data)
            env.add_appointment(appointment)
            link = '{}/appointment/{}'.format(request.host, appointment.get_id())
            flash('Appointment created. Link to share: {}'.format(link), category='success')
            return redirect('/sign_up')
    return render_template('creation_form.html', time_ranges=time_ranges, **form_data)


@app.route('/appointment/<id>', methods=('GET', 'POST'))
def appointment_details(id):
    appointment = env.get_appointment(id)
    form_data = {'full_name': '', 'email': ''}
    if request.method == 'POST':
        full_name = request.form.get('full_name', '')
        email = request.form.get('email', '')
        date = request.form.get('selected_date', '')
        initial_time = request.form.get('selected_time', '')

        form_data['full_name'] = full_name
        form_data['email'] = email
        form_data['date'] = date

        if not date or not initial_time or not full_name or not email:
            flash('All fields should be filled', category='danger')
        else:
            parsed_time = parse_time(initial_time)
            form_data['time'] = parsed_time

            env.add_participant(id, form_data)
            flash('Successfully submitted', category='success')
            return redirect('/success')
    return render_template('invitation_form.html', appointment=appointment, **form_data)


@app.route('/appointment/<id>/log_in', methods=('GET', 'POST'))
def log_in(id):
    if request.method == 'POST':
        user = request.form.get('login', '')
        if not env.user_verification(user):
            flash('You have not permissions to log in', category='danger')
        else:
            return redirect('/appointment/{}/participants'.format(id))
    return render_template('login.html')


@app.route('/appointment/<id>/participants')
def show_participants(id):
    appointment = env.get_appointment(id)
    return render_template('participants_list.html', subject=appointment.subject,
                           participants=appointment.participants)
