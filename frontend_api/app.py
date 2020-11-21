from flask import Flask, jsonify
from flask_restful import Api, Resource,abort,reqparse
from flasgger import Swagger, swag_from

app = Flask(__name__)
api = Api(app)
app.config['SWAGGER'] = {
    'title' : 'Central Medical Record',
    'uiversion' : 2
}
swag = Swagger(app)

patient = {
    '1001' : {"name" : "Ramesh", "age" : 22},
    '1002' : {"name" : "Raju","age": 34},
    '1003' : {"name" : "Narkasur","age":33}
 }

def abort_if_no_patient(patient_id):
    if patient_id not in patient:
        abort(404, message= "Patient {} dosen't exist in the database".format(patient_id))


parser = reqparse.RequestParser()
parser.add_argument('name',type = str)
parser.add_argument('age',type = int)

class patient_data(Resource):
    # Getting the patient info
    def get(self,patient_id):
        """
        Patient Info
        ---
        tags:
            - Getting Patient Data
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
                age:
                  type: integer
                name:
                  type: string

        """
        abort_if_no_patient(patient_id)
        return patient[patient_id]

    # Deleting a patient info
    def delete(self,patient_id):
        """
        Delete info
        ---
        tags:
          - Updating Patient Data
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
        del patient[patient_id]
        return 'Patient deleted',204

    # updating patient data
    def put(self,patient_id):
        """
        Updating patient info
        ---
        tags:
          - Updating Patient Data
        parameters:
          - in: body
            name: body
            schema:
              $ref : '#/definitions/Patient_data'
          - in: path
            name: patient_id
            required: true
            description: The Id of the Patient
            type: string
        responses:
          201:
            description: The patient data has been updated
            schema:
              $ref : '#/definitions/Patient_data'
        """
        args = parser.parse_args()
        patient_data = {'name':args["name"],'age':args["age"]}
        patient[patient_id] = patient_data
        return patient_data,201


class patient_list(Resource):
    def get(self):
        """
        To return all the patient data {TO BE REMOVED LATER}
        ---
        tags:
          - Getting Patient Data
        responses:
          200:
            description: The patient Data
            schema:
              id: patient_data
              properties:
                patient_id:
                    type: object
                    schema:
                      $ref : '#/definitions/Patient_data'
        """
        return patient

    def post(self):
        """
        Adding new Patient records
        ---
        tags:
            - Updating Patient Data
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
        patient_id = str(int(max(patient.keys()))+1)
        patient[patient_id] = {"name":args['name'],"age":args['age']}
        return patient[patient_id],201


api.add_resource(patient_data,'/patient_data/<patient_id>')
api.add_resource(patient_list,'/patient_list')

if __name__ == '__main__':
    app.run(debug=True)