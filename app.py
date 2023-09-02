from flask import Flask, Markup, make_response, Response, flash
from flask import render_template
from flask import redirect
from flask import url_for
from flask_mysqldb import MySQL
from flask import request
from flask import session
from flask_mail import Mail, Message
from config import mail_username, mail_password

# from flask import bcrypt

import re
import pandas as pd
import numpy as np
import pickle

from werkzeug.security import generate_password_hash, check_password_hash

from utils.fertilizer import fertilizer_dic

# import session
# import sklearn
# import sklearn as sk


app = Flask(__name__)

loaded_modelRFC = pickle.load(open('modelRFC.pkl', 'rb'))
loaded_modelNB = pickle.load(open('modelNB.pkl', 'rb'))
loaded_modelDT = pickle.load(open('modelDT.pkl', 'rb'))
loaded_modelKNN = pickle.load(open('modelKNN.pkl', 'rb'))

accuracy_valueRFC = pickle.load(open('accuracy_modelRFC.pkl', 'rb'))
accuracy_valueNB = pickle.load(open('accuracy_modelNB.pkl', 'rb'))
accuracy_valueDT = pickle.load(open('accuracy_modelDT.pkl', 'rb'))
accuracy_valueKNN = pickle.load(open('accuracy_modelKNN.pkl', 'rb'))

# any name that is super secret key
# app.secret_key = "super secret key"
app.secret_key = 'login'

app.config['MYSQL_Host'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_project'

app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password

mysql = MySQL(app)
mail = Mail(app)


def is_valid_credentials(email, password):
    # Function to check if the credentials are valid (query the database)
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user is not None:
        stored_hashed_password = user[4]  # Access password using index
        if check_password_hash(stored_hashed_password, password):
            return True

    return user is not None


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if is_valid_credentials(email, password):
            # Successful login
            session['loggedin'] = True
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            # Invalid credentials, return an error message
            msg = "Invalid credentials. Please try again."

    # GET request, show the login page
    return render_template('admintemplates/login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return render_template("admintemplates/login.html")


# ROUTESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS


@app.route('/register_controller', methods=["POST", "GET"])
def register_controller():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']

        # Email validation
        if not is_valid_email(email):
            error_msg = "Invalid email address use'@' "
            return render_template("admintemplates/register.html", error_msg=error_msg)

        hashed_password = generate_password_hash(password, method='sha256')
        myCursor = mysql.connection.cursor()

        # Check if the email already exists in the database
        myCursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = myCursor.fetchone()

        if existing_user:
            error_msg = "Account with this email already exists"
            return render_template("admintemplates/register.html", error_msg=error_msg)

        myCursor.execute("insert into users(fname, lname, email, password) values(%s, %s, %s, %s)",
                         (fname, lname, email, hashed_password))
        mysql.connection.commit()
        success_msg = "Account created successfully"
        return render_template("admintemplates/register.html", success_msg=success_msg)
    return render_template("admintemplates/register.html")


def is_valid_email(email):
    # Basic email validation using regex
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


###### STARTING TEMPLATE ROUTINGS ########
@app.route('/')
def index():
    myCursor = mysql.connection.cursor()
    myCursor.execute("select*from crops")
    data = myCursor.fetchall()
    myCursor.close()
    # return data will show an error do not try this 
    return render_template('startingtemplates/index.html', data=data)


@app.route("/about")
def about():
    return render_template("startingtemplates/about.html")


@app.route('/crops')
def crops():
    myCursor = mysql.connection.cursor()
    myCursor.execute("select*from crops")
    data = myCursor.fetchall()
    myCursor.close()
    # return data will show an error do not try this 
    return render_template('startingtemplates/crops.html', data=data)


@app.route("/team")
def team():
    return render_template("startingtemplates/team.html")


@app.route("/clients")
def clients():
    return render_template("startingtemplates/clients.html")


@app.route("/testing")
def testing():
    return render_template("startingtemplates/testing.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        msg = Message(subject=f"mail form {subject}", body=f"Name:{name}\nE-mail: {email}\n\n\n{message}",sender= mail_username,recipients=['arts10040@gmail.com'])
        mail.send(msg)
        return render_template("startingtemplates/contact.html", success=True)

    return render_template("startingtemplates/contact.html")


@app.route('/predict', methods=['POST'])
def predict():
    N = int(request.form['n'])
    P = int(request.form['p'])
    K = int(request.form['k'])
    temp = float(request.form['t'])
    humidity = float(request.form['h'])
    ph = float(request.form['ph'])
    rainfall = float(request.form['r'])

    # numpy array ma convert gareko
    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)

    predictionRFC = loaded_modelRFC.predict(single_pred)
    predictionNB = loaded_modelNB.predict(single_pred)
    predictionDT = loaded_modelDT.predict(single_pred)
    predictionKNN = loaded_modelKNN.predict(single_pred)

    # print(accuracy_valueRFC)
    # print(accuracy_valueNB)
    # print(accuracy_valueDT)
    # print(accuracy_valueKNN)

    crop_dict = {
        1: "Rice",
        2: 'Maize',
        3: 'Jute',
        4: 'Cotton',
        5: 'Coconut',
        6: 'Papaya',
        7: 'Orange',
        8: 'Apple',
        9: 'Muskmelon',
        10: 'Watermelon',
        11: 'Grapes',
        12: 'Mango',
        13: 'Banana',
        14: 'Pomegranate',
        15: 'Lentil',
        16: 'Blackgram',
        17: 'Mungbean',
        18: 'Mothbeans',
        19: 'Pigeonpeas',
        20: 'Kidneybeans',
        21: 'Chickpea',
        22: 'Coffee'
    }
    if predictionRFC[0] in crop_dict:
        crop = crop_dict[predictionRFC[0]]
        resultRFC = "{} is the best crop".format(crop)
    else:
        resultRFC = "Please try again..."

    if predictionNB[0] in crop_dict:
        # print("name"+ str(predictionNB[0]))
        # print(predictionNB)
        crop = crop_dict[predictionNB[0]]
        resultNB = "{} is the best crop".format(crop)
    else:
        resultNB = "Please try again..."

    if predictionDT[0] in crop_dict:
        crop = crop_dict[predictionDT[0]]
        resultDT = "{} is the best crop".format(crop)
    else:
        resultDT = "Please try again..."

    if predictionKNN[0] in crop_dict:
        crop = crop_dict[predictionKNN[0]]
        resultKNN = "{} is the best crop".format(crop)
    else:
        resultKNN = "Please try again..."

    # return render_template('index.html', resultNB = resultNB)

    return render_template(
        'admintemplates/testing.html',
        resultRFC=resultRFC,
        resultNB=resultNB,
        resultDT=resultDT,
        resultKNN=resultKNN,
        accuracy_valueNB=accuracy_valueNB * 100,
        accuracy_valueKNN=accuracy_valueKNN * 100,
        accuracy_valueDT=accuracy_valueDT * 100,
        accuracy_valueRFC=accuracy_valueRFC * 100,
    )


# ADMIN ROUTES/////////////////////////////////
@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        email = session['email']
        name = email.split('@')[0]

        return render_template('admintemplates/dashboard.html', name=name)
    else:
        msg = "you need to login first to access the page!!"
    return render_template("admintemplates/login.html", msg=msg)


@app.route("/admin/parameters")
def admin_parameters():
    if 'email' in session:
        email = session['email']
        name = email.split('@')[0]

        return render_template('admintemplates/parameters.html', name=name)
    else:
        msg = "you need to login first to access the page!!"

    return render_template("admintemplates/login.html", msg=msg)


@app.route("/admin/testinomials")
def admin_testinomials():
    if 'email' in session:
        email = session['email']
        name = email.split('@')[0]

        return render_template('admintemplates/testinomials.html', name=name)
    else:
        msg = "you need to login first to access the page!!"

    return render_template("admintemplates/login.html", msg=msg)


@app.route('/register')
def register():
    return render_template('admintemplates/register.html')


@app.route('/admin/crops')
def admin_crops():
    myCursor = mysql.connection.cursor()
    myCursor.execute("select*from crops")
    data = myCursor.fetchall()
    myCursor.close()

    # return data will show an error do not try this
    return render_template("/admintemplates/crops.html", data=data)


@app.route("/admin/addcrops")
def addcrops():
    return render_template("entryforms/addcrops.html")


@app.route("/admin/editcrops/<id>", methods=['GET'])
def edit_crop(id):
    myCursor = mysql.connection.cursor()

    myCursor.execute('SELECT * FROM crops WHERE id = %s', (id,))
    data = myCursor.fetchall()
    myCursor.close()

    if len(data) == 0:
        flash('Crop not found', 'danger')
        return redirect(url_for('admin_crops'))

    return render_template("entryforms/editcrops.html", crop=data)


@app.route("/admin/updatecrop/<id>", methods=['POST'])
def update_crop(id):
    if request.method == 'POST':
        name = request.form['name']
        scientific_name = request.form['scientific_name']
        description = request.form['description']
        season = request.form['season']
        image_url = request.form['image_url']

        myCursor = mysql.connection.cursor()

        myCursor.execute(
            'UPDATE crops SET name = %s, scientific_name = %s, description = %s, season = %s, image_url = %s WHERE id = %s',
            (name, scientific_name, description, season, image_url, id))

        mysql.connection.commit()
        myCursor.close()

        flash('Crop Updated Successfully')
        return redirect(url_for('admin_crops'))  # Redirect to the crops list page


@app.route("/admin/testing")
def admin_testing():
    if 'email' in session:
        email = session['email']
        name = email.split('@')[0]

        return render_template('admintemplates/testing.html', name=name)
    else:
        msg = "you need to login first to access the page!!"

    return render_template("admintemplates/login.html", msg=msg)


@app.route('/admin/fertilizer')
def fertilizer_recommendation():
    if 'email' in session:
        email = session['email']
        name = email.split('@')[0]

        return render_template('admintemplates/fertilizer.html', name=name)
    else:
        msg = "you need to login first to access the page!!"
    return render_template('admintemplates/login.html', msg=msg)


@app.route('/addcrops', methods=["POST", "GET"])
def create():
    if request.method == "POST":
        name = request.form['name']
        scientific_name = request.form['scientific_name']
        description = request.form['description']
        image_url = request.form['image_url']
        season = request.form['season']
        myCursor = mysql.connection.cursor()
        myCursor.execute(
            "INSERT INTO crops(name, scientific_name, description, season, image_url) values(%s, %s, %s, %s, %s)",
            (name, scientific_name, description, season, image_url))
        mysql.connection.commit()
        myCursor.close()
        # return render_template("admintemplates/crops.html")
        # return "data inserted"
        return redirect(url_for('admin_crops'))


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if request.method == 'POST':
        # Connect to the database
        conn = mysql.connection
        cursor = conn.cursor()

        # Perform the deletion query
        delete_query = "DELETE FROM crops WHERE id = %s"
        cursor.execute(delete_query, (item_id,))
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        return redirect(url_for('admin_crops'))


# render fertilizer recommendation result page


@app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    title = 'Fertilizer Suggestion'

    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['pottasium'])
    # ph = float(request.form['ph'])

    df = pd.read_csv('fertilizer.csv')

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K
    temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
    max_value = temp[max(temp.keys())]
    if max_value == "N":
        if n < 0:
            key = 'NHigh'
        else:
            key = "Nlow"
    elif max_value == "P":
        if p < 0:
            key = 'PHigh'
        else:
            key = "Plow"
    else:
        if k < 0:
            key = 'KHigh'
        else:
            key = "Klow"

    response = Markup(str(fertilizer_dic[key]))

    return render_template('/admintemplates/fertilizer-result.html', recommendation=response)


if __name__ == '__main__':
    app.run(debug=True, port="8000")
