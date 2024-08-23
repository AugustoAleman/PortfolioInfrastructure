from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def autoNotification(name, surname, email, phone, timeestamp, received_message, sender):

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = sender
    message["Subject"] = f'💼 {name}, sent you a new message!'

    # Message body
    html = f'''\
    <html>
        <body>
            <p>Hi Octavio, <br>
                <br>
                You've received a new message in your portfolio. The details are as follows:<br>
                <br>
                <ul>
                    <li><b>Name: </b>{ name + ' ' + surname}</li>
                    <li><b>E-mail: </b>{ email }</li>
                    <li><b>Phone: </b>{ phone if len(phone) > 1 else 'No register'}</li>
                    <li><b>Time: </b>{ timeestamp }</li>
                    <li><b>Message: </b>{received_message} </li>
                </ul>
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
