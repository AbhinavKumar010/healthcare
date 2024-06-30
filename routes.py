from flask import render_template, redirect, url_for, request, flash
from app import app, db
from models import Patient, Appointment
from utils.reminders import send_reminder
from utils.nlp import process_symptoms
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        medical_history = request.form['medical_history']
        current_medications = request.form['current_medications']

        new_patient = Patient(
            name=name,
            email=email,
            password=password,
            medical_history=medical_history,
            current_medications=current_medications
        )
        db.session.add(new_patient)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/report_symptoms', methods=['GET', 'POST'])
def report_symptoms():
    if request.method == 'POST':
        symptoms = request.form['symptoms']
        response = process_symptoms(symptoms)

        flash(f'Symptom analysis: {response}', 'info')
        return redirect(url_for('report_symptoms'))

    return render_template('report_symptoms.html')

@app.route('/schedule_appointment', methods=['GET', 'POST'])
def schedule_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        appointment_time = request.form['appointment_time']
        details = request.form['details']

        appointment = Appointment(
            patient_id=patient_id,
            appointment_time=datetime.strptime(appointment_time, '%Y-%m-%d %H:%M:%S'),
            details=details
        )
        db.session.add(appointment)
        db.session.commit()

        flash('Appointment scheduled!', 'success')
        return redirect(url_for('schedule_appointment'))

    patients = Patient.query.all()
    return render_template('schedule_appointment.html', patients=patients)
