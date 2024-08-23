from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def autoResponse(name, email, sender):

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = email
    message["Subject"] = f'💻 {name}, thank you for reaching out.'

    # Message body
    html = f'''\
    <html>
        <body>
            <p>Hi { name },<br>
                <br>
                Thank you for getting in touch with me through my portfolio. I appreciate you taking the time to reach out!<br>
                <br>
                Your message has been received, and I'll get back to you as soon as possible. If your inquiry is urgent, feel free to reply to this email or contact me directly  through any of the channels described below.<br>
                <br>
                Looking forward to connecting with you soon.<br>
                <br>
                Best regards,<br>
                <br>
                <b>Octavio Augusto Aleman Esparza</b><br>
                <i>Computer Science and Technology Engineer</i><br>
                <b>Tecnológico de Monterrey</b><br>
                <br>
                <b>Phone: </b>+52 1 5554311082<br>
                <b>LinkedIn: </b><a href = 'www.linkedin.com/in/augusto-aleman'>www.linkedin.com/in/augusto-aleman</a><br>
                <b>Email: </b>oa.alemanesparza@gmail.com<br>
            </p>
        </body>
    </html>
    '''

    # Add Body to message
    textMessage = MIMEText(html, 'html')
    message.attach(textMessage)

    message = message.as_string()

    return message
