#!flask/bin/python
from app import app

CSRF_ENABLED = True
app.secret_key = 'hahahahahahahah--that-was-funny'
app.config['UPLOAD_FOLDER'] = 'app/static/products/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.run(debug=True, host='127.0.0.1') #remove host if you do not want it public
