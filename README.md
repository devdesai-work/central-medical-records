# central-medical-records
Accelethon 2.0 project
Central medical records is a proposed idea for the competition, the aim of this project is to create a central record for storing and retrieving medical records of individuals across the country.

This project is built in python Flask, using Swagger as REstful.

To use this application run the requirements.txt file form the frontend_api folder in your command promt as
```
pip install -r requirements.txt
```
Then run app.py
```
python app.py
```
Keep the app.py running and go to the browser and open the below link,

http://localhost:5000/apidocs/ 

Here is some sample data for test runs:

Patient personal info:
```
d_id:4
p_id:420
p_name:"Esmae Forrest"
dob:"91/01/30"
dov:"12/07/01"
gender:"Male"
marital_status:"Single"
occupation:"Radio & TV Newscaster"
address:"1916 Center Point Rd, Center Point AL 35215"
contact_num:"+1 208-687-4825"
emergency_num:"+1 201-636-4578"
```
Patient  Medical Info:
```
p_id:420
complaint:"skin_rash"
chronic:"Atherosclerosis"
fam_hist:"Rheumatoid arthritis"
habits:"Drinking"
weight:52
surgeries:"Prostatectomy"
allergies:"Soybeans"
```
Patient Lab Test recod:
```
p_id:420
bl_test:"Low RBC count"
micro_test:"Normal"
cyt_test:"Normal"
hl_p_test:"Normal"
cyg_test:"Normal"
ur_test:"Normal"
```
Patient Diagnosis Data:
```
p_id:856
diag_date:"96/01/07"
diagnosis:"Chronic cholestasis"
surg_req:"No"
```
