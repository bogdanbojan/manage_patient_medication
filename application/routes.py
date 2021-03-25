from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Patient, Medication



@app.route('/')
def index():
    return 'Hello'


@app.route('/patients')
def get_patients():
    """
    Returns all the patients from the database.

    :return: List containing the patients. It outputs patients' first name, last name and a short description.
    """

    patients = Patient.query.all()

    output = []
    for patient in patients:
        patient_data = {'firstName': patient.first_name, 'lastName': patient.last_name, 'description': patient.description}
        output.append(patient_data)
    return {"patients": output}

@app.route('/medications')
def get_medications():
    """
    Returns all the medications from the database.

    :return: List containing the medications. It outputs medications' description, dosage and unit.
    """

    medications = Medication.query.all()

    output = []
    for medication in medications:
        medication_data = {'description': medication.description, 'dosage': medication.dosage, 'unit': medication.unit}
        output.append(medication_data)
    return {"medications": output}

@app.route('/patients/<patient_id>')
def get_patient(patient_id):
    """
    Returns data about a specific patient.

    :param patient_id: The patients' database ID.
    :return: A json object that contains patient's first name, last name and a short description.
    """

    patient = Patient.query.get_or_404(patient_id)
    return {'firstName': patient.first_name, 'lastName': patient.last_name, "description": patient.description}

@app.route('/patients/<patient_id>/<medication_id>')
def get_medication(medication_id):
    """
    Return data about a specific medication.

    :param medication_id: The medications' database ID.
    :return: A json object that contains the medications' description, dosage and unit.
    """

    medication = Medication.query.get_or_404(medication_id)
    return {'description': medication.description, 'dosage': medication.dosage}

@app.route('/patients', methods=['POST'])
def add_patient():
    """
    Method to add a new patient to the database. Metod = POST

    **Json request parameters**:
    * firstName (string)
    * lastName (string)
    * description (string)
    * gender (enum)
    * dateOfBirth ('YYYY-MM-DD')
    * modifyDate (will be automated)

    ! gender is an enum type: ``male, female or unknown`` arguments accepted.

    :return: if the patient is added- a *successful* message
    """
    patient = Patient(first_name=request.json['firstName'],
                      last_name=request.json['lastName'],
                      description=request.json['description'],
                      gender=request.json['gender'],
                      date_of_birth=request.json['dateOfBirth'],
                      modify_date=request.json['modifyDate']
                      )
    db.session.add(patient)
    db.session.commit()
    return {'message': 'successful'}

@app.route('/patients/<patient_id>', methods=['POST'])
def add_medication(patient_id):
    """
    Method to add a new medication to the database. Method = POST

    **Json request parameters**:
    * description (string)
    * dosage (int)
    * unit (enum)
    * time ('HH:MM:SS')
    * creationDate ('YYYY-MM-DD')
    * modifyDate (will be automated)

    ! unit is an enum type: ``kg, g, mg,mcg, l, ml, cc, mol, mmol`` arguments accepted.

    :param patient_id: ID of the patient that you want to add medicine to.
    :return: if the medication is added- a *successful* message
    """
    medication = Medication(description=request.json['description'],
                            dosage=request.json['dosage'],
                            unit=request.json['unit'],
                            time=request.json['time'],
                            creation_date=request.json['creationDate'],
                            modify_date=request.json['modifyDate'],
                            patient=Patient.query.get_or_404(patient_id))
    db.session.add(medication)
    db.session.commit()
    return {'message': 'successful'}


@app.route('/patients/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """
    Deletes a patient based on his ID. Method = DELETE

    :param patient_id: The ID of the patient you want to delete.
    :return: If the patient is deleted- a *successful* message.
    """
    patient = Patient.query.get(patient_id)
    if patient is None:
        return {"error": "not found"}
    db.session.delete(patient)
    db.session.commit()
    return {"message": "Successful"}

@app.route('/patients/<patient_id>/<medication_id>', methods=['DELETE'])
def delete_medication(medication_id):
    """
    Deletes a medication based on its ID. Method = DELETE

    :param medication_id: The ID of the medication you want to delete.
    :return: If the medication is deleted- a *successful* message.
    """
    medication = Medication.query.get_or_404(medication_id)
    if medication is None:
        return {"error": "not found"}
    db.session.delete(medication)
    db.session.commit()
    return {"message": "Successful"}


@app.route('/patients/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """
    Updates data about a specific patient. Method = PUT

    **Available Json request parameters**:
    * firstName (string)
    * lastName (string)
    * description (string)
    * gender (enum)
    * dateOfBirth ('YYYY-MM-DD')
    * modifyDate (will be automated)

    ! gender is an enum type: ``male, female or unknown`` arguments accepted.

    :param patient_id:  The ID of the patient you want to delete.
    :return: If the patient is updated- a *successful* message.
    """
    patient = Patient.query.get_or_404(patient_id)
    if 'firstName' in request.json:
        patient.first_name = request.json['firstName']
    if 'lastName' in request.json:
        patient.last_name = request.json['lastName']
    if 'description' in request.json:
        patient.description = request.json['description']
    if 'gender' in request.json:
        patient.gender = request.json['gender']
    if 'dateOfBirth' in request.json:
        patient.date_of_birth = request.json['dateOfBirth']

    # patient.modify_date = current_date # add current date
    # db.session.add(patient)
    db.session.commit()
    return {"message": "Successful"}

@app.route('/patients/<patient_id>/<medication_id>',  methods=['PUT'])
def update_medication(medication_id):
    """
    Updates data about a specific medication. Method = PUT

    **Json request parameters**:
    * description (string)
    * dosage (int)
    * unit (enum)
    * time ('HH:MM:SS')
    * creationDate ('YYYY-MM-DD')
    * modifyDate (will be automated)

    ! unit is an enum type: ``kg, g, mg,mcg, l, ml, cc, mol, mmol`` arguments accepted.

    :param medication_id: The ID of the medication you want to update.
    :return: If the medication is updated- a *successful* message.
    """

    medication = Medication.query.get_or_404(medication_id)
    if 'description' in request.json:
        medication.description = request.json['description']
    if 'dosage' in request.json:
        medication.dosage = request.json['dosage']
    if 'unit' in request.json:
        medication.unit = request.json['unit']
    if 'time' in request.json:
        medication.time = request.json['time']

    db.session.commit()
    return {"message": "Successful"}
