# Import necessary dependencies
from flask import Flask, request, jsonify
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

# Starting Flask app
app = Flask(__name__)
CORS(app)  

# For DB connection to MySQL
db = mysql.connector.connect(
    host="localhost",
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE")
)

# Email login credentials
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
password_key = os.getenv('MAIL_PASSWORD')

# SMTP Server and port no for GMAIL.com
gmail_server = "smtp.gmail.com"
gmail_port = 587

# Starting email server connection
my_server = smtplib.SMTP(gmail_server, gmail_port)
my_server.ehlo()
my_server.starttls()
my_server.login(MAIL_USERNAME, password_key)

# /submit -> Receives form data from Frontend form
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
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
    
        # Send automated response
        my_server.sendmail(
            from_addr=MAIL_USERNAME,
            to_addrs=email,
            msg=autoResponse(name, email, MAIL_USERNAME)
        )
        
        # Send automated notification
        my_server.sendmail(
            from_addr=MAIL_USERNAME,
            to_addrs=MAIL_USERNAME,
            msg=autoNotification(name, surname, email, phone, now.strftime("%d-%m-%Y %H:%M:%S"), message, MAIL_USERNAME)
        )

        return jsonify({"message": "Data submitted successfully"}), 201
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run() 
