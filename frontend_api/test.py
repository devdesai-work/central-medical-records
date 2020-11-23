from pymongo import MongoClient

client = MongoClient("mongodb+srv://Pranav:mongodbisuseful@cluster0.3kcso.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client['medicalDB']
collection = db['Patient_personal_info']

data = {420 : []}
for x in collection.find({'p_id'  : 420}):
        data[420].append(x)

if collection.find({'p_id' : 420}).count() == 0:
        print("no 420")

print(data[420][0])