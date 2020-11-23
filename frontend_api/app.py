from flask import Flask, jsonify
from flask_restful import Api, Resource,abort,reqparse
from flasgger import Swagger, swag_from
from pymongo import MongoClient
import json
from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))



client = MongoClient("mongodb+srv://Pranav:mongodbisuseful@cluster0.3kcso.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client['medicalDB']
patient = db['Patient_personal_info']
patient_diagnosis_data = db['Diagnosis']
lab_test = db['Lab_tests_1']
patient_med_info = db['Patient_med_info']




app = Flask(__name__)
api = Api(app)
app.config['SWAGGER'] = {
    'title' : 'Central Medical Record',
    'uiversion' : 2
}
swag = Swagger(app)



def abort_if_no_patient(patient_id):
    if patient.find({'p_id' : int(patient_id)}).count() == 0:
        abort(404, message= "Patient {} dosen't exist in the database".format(patient_id))


parser = reqparse.RequestParser()
parser.add_argument('d_id',type = int)
parser.add_argument('p_id',type = int)
parser.add_argument('p_name',type= str)
parser.add_argument('dob',type= str)
parser.add_argument('dov',type= str)
parser.add_argument('gender',type= str)
parser.add_argument('marital_status',type= str)
parser.add_argument('occupation',type= str)
parser.add_argument('address',type= str)
parser.add_argument('contact_num',type= str)
parser.add_argument('emergency_num',type= str)
parser.add_argument('diag_date',type= str)
parser.add_argument('diagnosis',type= str)
parser.add_argument('surg_req',type= str)





class patient_data(Resource):
    # Getting the patient info

    def get(self,patient_id):
        """
        Patient Info
        ---
        tags:
          - Patient personal Data
        parameters:
          - name: patient_id
            in: path
            required: true
            description: ID of the Patient
            type: string
        responses:
          200:
            description: The Patient data
            schema:
              id: Patient_data
              properties:
                d_id:
                  type: integer
                p_id:
                  typr: integer
                p_name:
                  type: string
                dob:
                  type: string
                dov:
                  type: string
                gender:
                  type: string
                marital_status:
                  type: string
                occupation:
                  type: string
                address:
                  type: string
                contact_num:
                  type: string
                emergency_num:
                  type: string

        """
        data = {patient_id : []}
        abort_if_no_patient(patient_id)
        for x in patient.find({'p_id'  : int(patient_id)}):
            data[patient_id].append(x)
        val = parse_json(data[patient_id][0])
        return val


    # Deleting a patient info
    def delete(self,patient_id):
        """
        Delete info
        ---
        tags:
          - Patient personal Data
        parameters:
          - in: path
            name: patient_id
            required: true
            description: The ID of the Patient
            type: string
        response:
          204:
            description: Patient info deleted
        """
        abort_if_no_patient(patient_id)
        patient.delete_one({'p_id':int(patient_id)})
        return 'Patient deleted',204

class patient_list(Resource):
    def post(self):
        """
        Adding new Patient records
        ---
        tags:
            - Patient personal Data
        parameters:
          - in: body
            name: body
            schema:
              $ref : '#/definitions/Patient_data'
        responses:
          201:
            description: New Patient added to records
            schema:
              $ref : '#/definitions/Patient_data'
        """
        args = parser.parse_args()
        patient_id = args['p_id']
        patient.insert_one(args)
        data = {patient_id: []}
        for x in patient.find({'p_id': int(patient_id)}):
            data[patient_id].append(x)
        val = parse_json(data[patient_id][0])

        return val,201


class new_diagnosis(Resource):
    def post(self):
        """
        Adding new Patient records
        ---
        tags:
            - Patient Diagnosis Data
        parameters:
          - in: body
            name: body
            schema:
              id: Patient_diagnosis
              properties:
                p_id:
                  type: integer
                diag_date:
                  type: string
                diagnosis:
                  type: string
                surg_req:
                  type: string
        responses:
          201:
            description: New diagnosis
            schema:
              id: Patient_diagnosis
              properties:
                p_id:
                  type: integer
                diag_date:
                  type: string
                diagnosis:
                  type: string
                surg_req:
                  type: string
        """
        args = parser.parse_args()
        patient_id = args['p_id']
        patient.insert_one(args)
        data = {patient_id: []}
        for x in patient_diagnosis_data.find({'p_id': int(patient_id)}):
            data[patient_id].append(x)
        val = parse_json(data[patient_id][0])

        return val, 201


class patient_diagnosis(Resource):

    def get(self,patient_id):
        """
        Patient Info
        ---
        tags:
          - Patient Diagnosis Data
        parameters:
          - name: patient_id
            in: path
            required: true
            description: ID of the Patient
            type: string
        responses:
          200:
            description: The Patient data
            schema:
              id: Patient_diagnosis
              properties:
                p_id:
                  type: integer
                diag_date:
                  type: string
                diagnosis:
                  type: string
                surg_req:
                  type: string

        """
        data = {patient_id : []}
        abort_if_no_patient(patient_id)
        for x in patient_diagnosis_data.find({'p_id'  : int(patient_id)}):
            data[patient_id].append(x)
        val = parse_json(data[patient_id][0])
        return val


    # Deleting a patient info
    def delete(self,patient_id):
        """
        Delete info
        ---
        tags:
          - Patient Diagnosis Data
        parameters:
          - in: path
            name: patient_id
            required: true
            description: The ID of the Patient
            type: string
        response:
          204:
            description: Patient info deleted
        """
        abort_if_no_patient(patient_id)
        patient_diagnosis_data.delete_one({'p_id':int(patient_id)})
        return 'Patient deleted',204

class lab_test_results(Resource):
    def get(self,patient_id):
        """
        Patient Info
        ---
        tags:
          - Lab Test
        parameters:
          - name: patient_id
            in: path
            required: true
            description: ID of the Patient
            type: string
        responses:
          200:
            description: The Patient data
            schema:
              id: Patient_diagnosis
              properties:
                p_id:
                  type: integer
                bl_test:
                  type: string
                micro_test:
                  type: string
                cyt_test:
                  type: string
                hl_p_test:
                  type: string
                cyg_test:
                  type: string
                ur_test:
                  type: string

        """
        data = {patient_id : []}
        abort_if_no_patient(patient_id)
        for x in lab_test.find({'p_id'  : int(patient_id)}):
            data[patient_id].append(x)
        val = parse_json(data[patient_id][0])
        return val


    # Deleting a patient info
    def delete(self,patient_id):
        """
        Delete info
        ---
        tags:
          - Lab Test
        parameters:
          - in: path
            name: patient_id
            required: true
            description: The ID of the Patient
            type: string
        response:
          204:
            description: Patient info deleted
        """
        abort_if_no_patient(patient_id)
        lab_test.delete_one({'p_id':int(patient_id)})
        return 'Patient deleted',204

class patient_medical_info(Resource):
    def get(self,patient_id):
        """
        Patient Info
        ---
        tags:
          - Patient Medical Info
        parameters:
          - name: patient_id
            in: path
            required: true
            description: ID of the Patient
            type: string
        responses:
          200:
            description: The Patient data
            schema:
              id: Patient_diagnosis
              properties:
                p_id:
                  type: integer
                complaint:
                  type: string
                chronic:
                  type: string
                fam_hist:
                  type: string
                habits:
                  type: string
                weight:
                  type: string
                surgeries:
                  type: string
                allergies:
                  type: string

        """
        data = {patient_id : []}
        abort_if_no_patient(patient_id)
        for x in patient_med_info.find({'p_id'  : int(patient_id)}):
            data[patient_id].append(x)
        val = parse_json(data[patient_id][0])
        return val


    # Deleting a patient info
    def delete(self,patient_id):
        """
        Delete info
        ---
        tags:
          - Patient Medical Info
        parameters:
          - in: path
            name: patient_id
            required: true
            description: The ID of the Patient
            type: string
        response:
          204:
            description: Patient info deleted
        """
        abort_if_no_patient(patient_id)
        patient_med_info.delete_one({'p_id':int(patient_id)})
        return 'Patient deleted',204








api.add_resource(patient_data,'/patient_data/<patient_id>')
api.add_resource(patient_diagnosis,'/patient_diagnosis/<patient_id>')
api.add_resource(patient_list,'/patient_list')
api.add_resource(new_diagnosis,'/new_diagnosis')
api.add_resource(lab_test_results,'/lab_test_results/<patient_id>')
api.add_resource(patient_medical_info,'/patient_medical_info/<patient_id>')

if __name__ == '__main__':
    app.run(debug=True)