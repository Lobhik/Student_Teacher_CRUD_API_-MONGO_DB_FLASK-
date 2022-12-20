from bson import ObjectId
from flask import Flask, jsonify, request, redirect
from flask.helpers import url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/clg"
mongo = PyMongo(app)
#all techers 
@app.route('/', methods = ['GET'])
def retrieveAll():
    holder = list()
    currentCollection = mongo.db.all_teachers
    for i in currentCollection.find():
        print(i)
        holder.append( {
            "id": i["id"],
            "teacher_name": i["teacher_name"],
            "course": i["course"]
        })
    return jsonify({'test':holder})

#all students with specific course and teacher
@app.route('/<teacher_name>', methods = ['GET'])
def retrieveFromName(teacher_name):
    holder = list()
    currentCollection = mongo.db.all_teachers
    data = currentCollection.find_one({"teacher_name" : teacher_name})
    if data:
        print(data['course'])
        studentCollection = mongo.db.all_students
        for i in studentCollection.find({"course":data['course']}):
            print(i)
            holder.append( {
                    "roll_no": i["roll_no"],
                    "name": i["name"],
                    "last_name": i["last_name"],
                    "course": i["course"]
                })
        return jsonify({teacher_name: holder})
    else:
        return jsonify({"fail"})

#adding teachers
@app.route('/', methods = ['POST'])
def postData():
    currentCollection = mongo.db.all_teachers
    _id = request.json['id']
    
    teacher_name = request.json['teacher_name']
    course = request.json['course']
    if _id and teacher_name and course and request.method == 'POST':

        currentCollection.insert_one({'id' : _id, 'teacher_name' : teacher_name, 'course' : course})
        return jsonify("Successfully added")
    else:
        return jsonify("Invalid data")


#delating specific teacher
@app.route('/<teacher_name>', methods = ['DELETE'])
def deleteData(teacher_name):
    currentCollection = mongo.db.all_teachers
    currentCollection.delete_one({'teacher_name' : teacher_name})
    return redirect(url_for('retrieveAll'))




#all students data
@app.route('/all_students', methods = ['GET'])
def all_students():
    holder = list()
    students = mongo.db.all_students
    for i in students.find():
        print(i)
        holder.append( {
            "roll_no": i["roll_no"],
            "name": i["name"],
            "last_name": i["last_name"],
            "course": i["course"]
        })
    return jsonify({'students':holder})



#adding  students to specific course

@app.route('/add_students', methods = ['POST'])
def post_students():
    students = mongo.db.all_students
    roll_no = request.json['roll_no']
    course = request.json['course']
    name = request.json['name']
    last_name = request.json['last_name']
    if roll_no and name and last_name and request.method == 'POST':

        students.insert_one({'name' : name, 'roll_no' : roll_no, 'last_name' : last_name, 'course': course})
        return jsonify("Successfully added")
    else:
        return jsonify("Invalid data")


#db.student.updateMany({'_id': ObjectId('6375e1babfafc17d2d207ace')}, {"$set" : {'teacher_name' : "lalita", "subject" : "math"}})


#updating teachers details
@app.route('/tea_update/<id>', methods = ['PUT'])
def updateData(id):
    currentCollection = mongo.db.all_teachers
    updatedName = request.json['teacher_name']
    updatecourse =request.json['course']
    currentCollection.update_one({'id': id}, {"$set" : {'course' : updatecourse}})
    return jsonify("updated successfully")



#updating student details 
@app.route('/std_update/<roll_no>', methods = ['PUT'])
def updatedata(roll_no):
    currentCollection = mongo.db.all_students
    updatecourse = request.json['course']
    print(updatecourse)
    currentCollection.update_one({'roll_no': roll_no}, {"$set" : {'course' : updatecourse}})
    return jsonify("updated successfully")





if __name__ == '__main__':
    app.run(debug = True)



"""
db.student.updateOne({"students.std_no" : 5}, {$set : {"students.$.name" : "akshay"}})
db.student.updateOne({"_id ": ObjectId('6375e1dabfafc17d2d207ad0')}, {$set : {"students.$.name" : "ram"}})
db.student.updateOne({"_id" : ObjectId('6375e1dabfafc17d2d207ad0'), "students.std_no" : 5}, {$push : {students : {$each : [{"std_no" : 6, "name" : "avinash"}]}}})
db.student.updateOne({"_id" : ObjectId('6375e1dabfafc17d2d207ad0')}, {$push : {students : {$each : [{"std_no" : 6, "name" : "priya"}]}}})
Find query
db.Demo.find({"_id" : ObjectId('637719d99e0678b607dec724'), "students.name": "prajot" } )




"""


