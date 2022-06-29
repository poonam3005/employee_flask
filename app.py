import os
from select import select
from sqlite3 import Cursor
from flask import Flask,render_template, request,redirect, send_from_directory, url_for
import psycopg2

app = Flask(__name__)


def connection():
    host = 'localhost' 
    database = 'sql_demo' 
    user = 'postgres' 
    password = '12345'
    conn = psycopg2.connect(host=host, user=user, password=password, database=database)
    return conn



UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["IMAGE_UPLOADS"] = "D:\Flask\employee\static"
app.config['UPLOAD_DIRECTORY'] = 'static/'


# --------RETRIVE--------

@app.route('/')
def list():
    emp1 =[]
    conn = connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM employee where delete='false'")

    for row in cursor.fetchall():
        emp1.append({"id": row[0], "name": row[1], "code": row[2], "bday": row[3], "gender": row[4], "position": row[5], "age": row[6], "hobby": row[7], "address": row[8], "image": row[9]})
        print(emp1)
    conn.close()
    print('.............')
    return render_template("list.html", emp1 = emp1)

# --------RETRIVE WITH ID--------

@app.route('/datalist/<int:id>' , methods = ['GET','POST'])
def datalist(id):
    emp1 =[]
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee where id=%s",(str(id)))
    for row in cursor.fetchall():
        emp1.append({"id": row[0], "name": row[1], "code": row[2], "bday": row[3], "gender": row[4], "position": row[5], "age": row[6], "address": row[7], "image": row[8]})
        print(emp1)
    conn.close()
    return render_template("list.html", emp1 = emp1)


# --------CREATE--------

@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')

    if request.method=='POST':
        id=request.form['id']
        name=request.form['name']
        code=request.form['code']
        bday=request.form['bday']
        gender=request.form['gender']
        position=request.form['position']
        age=request.form['age']
        hobby=request.form['hobby']
        address=request.form['address']

        if request.files:
            image = request.files['image']
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            return render_template("create.html", uploaded_image=image.filename)
            

        conn = connection()
        cursor = conn.cursor()
     

        cursor.execute("INSERT INTO employee ( id,name, code, bday, gender, position, age, hobby, address) VALUES (  %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id,name, code, bday, gender, position, age, hobby, address))
        print('===========')

        conn.commit()
        conn.close()
        return redirect('/')


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)


# @app.route('/display/<filename>')
# def display_image(filename):
# 	return redirect(url_for('static', filename='uploads/' + filename), code=301)



# --------UPDATE--------


@app.route('/update/<int:id>' , methods = ['GET','POST'])
def update(id):
    e=[]
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM employee where id=%s",(str(id)))
        for row in cursor.fetchall():
            e.append({"id": row[0], "name": row[1], "code": row[2], "bday": row[3], "gender": row[4], "position": row[5], "age": row[6], "hobby": row[7], "address": row[8], "image": row[9]})
        conn.close()
        return render_template("update.html",e=e[0])  

    if request.method=='POST':
        id=request.form['id']
        name=request.form['name']
        code=request.form['code']
        bday=request.form['bday']

        gender=request.form['gender']
        position=request.form['position']
        age=request.form['age']

        # hobby=str(request.form.getlist('hobby'))
        hobby=request.form.getlist('hobby')
        print(hobby)
        
        address=request.form['address']
        image=request.form['image']
        print('image:', image)

       
        cursor.execute("update employee set name=%s, code=%s, bday=%s, gender=%s, position=%s, age=%s, hobby=%s, address=%s,image=%s where id=%s",(name, code, bday, gender, position, age, hobby,address,image, id))
        conn.commit()
        conn.close()
        return redirect('/')




# --------DELETE--------


@app.route('/delete/<int:id>' , methods = ['GET','POST'])
def delete(id):
    
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("update employee set delete='true' where id=%s",[id])
        
        conn.commit()
        conn.close()
        return redirect("/")  

    






# app.config["IMAGE_UPLOADS"] = "D:\Flask\employee\static"



# --------UPLOAD SINGLE IMAGE --------


# Route to upload image
@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            return render_template("upload.html", uploaded_image=image.filename)
    return render_template("upload.html")


@app.route('/uploads/<filename>')
def send_uploaded_file1(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)




if __name__ == '__main__':
    app.run(debug=True)