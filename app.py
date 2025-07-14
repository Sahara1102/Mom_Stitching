import os
from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message

app = Flask(__name__)

# Email configuration using environment variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')  # Needed!

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message(
            subject=f"Message from {name}",
            sender=app.config['MAIL_DEFAULT_SENDER'],  # Now always safe
            recipients=[app.config['MAIL_USERNAME']],  # Your receiving email
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )

        mail.send(msg)
        return redirect('/')
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
