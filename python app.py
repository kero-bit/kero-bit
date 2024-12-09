from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
db = SQLAlchemy(app)

# Models
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    doctor_name = db.Column(db.String(100))

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    treatment_type = db.Column(db.String(100))
    cost = db.Column(db.Float)

# CRUD Endpoints
@app.route('/patients', methods=['POST', 'GET'])
def handle_patients():
    if request.method == 'POST':
        data = request.json
        new_patient = Patient(name=data['name'], age=data['age'], phone=data['phone'], email=data['email'])
        db.session.add(new_patient)
        db.session.commit()
        return jsonify({"message": "Patient added successfully"}), 201

    elif request.method == 'GET':
        patients = Patient.query.all()
        return jsonify([{"id": p.id, "name": p.name, "age": p.age, "phone": p.phone, "email": p.email} for p in patients])

@app.route('/patients/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_patient(id):
    patient = Patient.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify({"id": patient.id, "name": patient.name, "age": patient.age, "phone": patient.phone, "email": patient.email})

    elif request.method == 'PUT':
        data = request.json
        patient.name = data['name']
        patient.age = data['age']
        patient.phone = data['phone']
        patient.email = data['email']
        db.session.commit()
        return jsonify({"message": "Patient updated successfully"})

    elif request.method == 'DELETE':
        db.session.delete(patient)
        db.session.commit()
        return jsonify({"message": "Patient deleted successfully"})

# More endpoints for Appointments and Treatments follow the same pattern.

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
