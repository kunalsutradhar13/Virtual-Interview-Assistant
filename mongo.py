import pymongo
from pymongo import MongoClient
import pprint
import json
client = MongoClient('localhost', 27017)
db = client['question-database']
collection = db['questions']

doc1 = { "key": "Android",
		 "questions" : [ "who uses Android?", "name of Android Founder?"] }
doc2 = { "key" : "Agile",
		 "questions" : ["how many weeks is a sprint?", "who is scrummmaster??"] }
doc3 = { "key" : "Operating Systems",
		 "questions" : ["name flavors of linux?", "what is a kernel??"] }
doc4 = { "key" : "Java",
		 "questions" : ["inheritance?", "polymorphism?"] }

post_id = collection.insert_one(doc1).inserted_id
post_id = collection.insert_one(doc2).inserted_id
post_id = collection.insert_one(doc3).inserted_id
post_id = collection.insert_one(doc4).inserted_id
str1 = '{"$or":['
str2 = '{"key": {"$regex": "Android", "$options": "i"}},'
str3 = '{"key": {"$regex": "Agile", "$options": "i"}}'
str4 = ']}'
strFinal= str1+str2+str3+str4
#print strFinal

Questionset = set()
questions = db.questions.find(json.loads(strFinal))
for item in questions:
	valList = item["questions"]
	for it in valList:
		Questionset.add(it)

for i in Questionset:
	print(i)
str1= "many fancy word hello hi"
listValues = str1.split()
