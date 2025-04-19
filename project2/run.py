from flask import Flask,jsonify,request ,render_template, send_from_directory
from app.database import get_db
from datetime import datetime


user_collection = get_db()['users']
calc_collection = get_db()['calculations']
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/<page>')
def serve_page(page):
    return send_from_directory('templates', page)

@app.route("/register",methods=["POST"])
def register():
    user_data= request.form
    name=user_data.get("name","")
    username=user_data.get("username","")
    password=user_data.get("password","")
    email_id=user_data.get("email_id","")
    mobile_number=user_data.get("mobile_number","")
    dob=user_data.get("dob","")
    
    response= user_collection.find_one({"email_id":email_id})
    if not response:
        user_collection.insert_one({"Name":name,"username":username,"password": password,"email_id":email_id,
                                    "mobile_number":mobile_number,"dob":dob})
        return jsonify({"status":"success","message":"user registered successfully"})
    
    else:
        return jsonify({"status":"error","message":"user already exists"})
    
@app.route("/login",methods=["POST"])
def login():
    user_data=request.form
    username=user_data.get("username","")
    password=user_data.get("password","")
    response= user_collection.find_one({"username":username,"password":password})
    if response:
        return jsonify({"status":"success","message":" login sucessfull"})
    else:
        return jsonify({"status":"error","message":"invalid credentials"})
    
@app.route('/forgot', methods = ['POST'])
def forgot_password():
    user_data = request.form
    email_id = user_data.get('email_id', '')
    dob = user_data.get('dob','')
    new_password = user_data.get('new_password','')
    response =  user_collection.find_one({'email_id':email_id,'dob':dob})
    if response:
        user_collection.update_one({'email_id':email_id,'dob':dob}, 
                                   {"$set": {'password':new_password}})
        
        return jsonify({"status": 'Success', "message" :  "Password updated successfully"})
    
    else:
        return jsonify({"status": 'Error', "message" :  "User not exist"})


@app.route('/calculator', methods = ['POST'])
def calculator():
    data = request.form
    username = data.get('username')
    x = float(data['x'])
    y = float(data['y'])
    operation = data['operation']
    if operation == 'addition':
        result = x + y
    
    elif operation == 'multiplication':
        result = x * y

    elif operation == 'subtraction':
        result = x - y

    elif operation == 'division':
        result = x / y
    
    

    calc_collection.insert_one({
        "username": username,
        "operation_type": operation,
        "operand1": x,
        "operand2": y,
        "result": result,
        "timestamp": datetime.utcnow()
    })

    return jsonify({"status": "success", "result": result})


@app.route('/history/<username>', methods=['GET'])
def get_history(username):
    records = list(calc_collection.find({"username": username}, {"_id": 0}))
    return jsonify({"status": "success", "history": records})


@app.route('/clear-history/<username>', methods=['DELETE'])
def clear_history(username):
    calc_collection.delete_many({"username": username})
    return jsonify({"status": "success", "message": "History cleared successfully"})


   
    
if __name__=="__main__":
    app.run(port=5006,debug=True)
    