# Import necessary dependencies
from flask import Flask, request, jsonify, send_file, make_response
import mysql.connector
from flask_cors import CORS

import smtplib 
from email_response.auto_response import autoResponse
from email_response.auto_notification import autoNotification

from dotenv import load_dotenv
from datetime import datetime
import os

# Loading environment variables
load_dotenv()

# For DB connection to MySQL
db = mysql.connector.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE")
)

# Starting Flask app
app = Flask(__name__)
CORS(app)  

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Flask app!"

# /submit -> Receives form data from Frontend form
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Establish a new database connection for this request
        db = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE")
        )

        # Parse JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        name = data.get('name')
        surname = data.get('surname')
        email = data.get('email')
        phone = data.get('phone')
        message = data.get('message')

        # Current timestamp
        now = datetime.now()

        # Insert data into the MySQL database
        cursor = db.cursor()
        sql = "INSERT INTO forms (name, surname, email, phone, message, sent_date) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, surname, email, phone, message, now)

        cursor.execute(sql, values)
        db.commit()

        # Close the cursor and the connection
        cursor.close()
        db.close()

        # Email login credentials
        MAIL_USERNAME = os.getenv('MAIL_USERNAME')
        password_key = os.getenv('MAIL_PASSWORD')

        # SMTP Server and port no for GMAIL.com
        gmail_server =  os.getenv('EMAIL_SERVER')
        gmail_port = 587

        # For automated emails

        # Starting email server connection
        my_server = smtplib.SMTP(gmail_server, gmail_port)
        my_server.ehlo()
        my_server.starttls()
        my_server.login(MAIL_USERNAME, password_key)
    
        # Send automated response
        my_server.sendmail(
            from_addr=MAIL_USERNAME,
            to_addrs=email,
            msg=autoResponse(name, surname, email, MAIL_USERNAME)
        )
        
        # Send automated notification
        notification_mail = os.getenv('NOTIFICATION_MAIL')
        my_server.sendmail(
            from_addr=MAIL_USERNAME,
            to_addrs=notification_mail,
            msg=autoNotification(name, surname, email, phone, now.strftime("%d-%m-%Y %H:%M:%S"), message, MAIL_USERNAME, notification_mail)
        )

        # Close the email server connection
        my_server.quit()

        return jsonify({"message": "Data submitted successfully"}), 201
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
# /download -> returns resume file
@app.route('/download', methods=['GET'])
def download():
    try:
        file_path = './files/resume.pdf'
        response = make_response(send_file(file_path, as_attachment=True))
        response.headers['Content-Disposition'] = 'attachment; filename=resume.pdf'
        return response
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))
