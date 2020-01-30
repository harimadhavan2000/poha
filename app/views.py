from app import app
from flask import request, render_template, jsonify, abort, make_response, flash, url_for, send_from_directory
import re
import os
import json
from .forms import product_submit
#import forms
i=0
from werkzeug import secure_filename
from flask import Flask, redirect,  request, session
from flask_oauthlib.client import OAuth
app.config['GOOGLE_ID'] = "438432736772-4tq1lq7ef88j57d2tdji6nmom7620gon.apps.googleusercontent.com"
app.config['GOOGLE_SECRET'] = "kvBsEE4th9NQXy3BygQ9WG1d"
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def data(sku, name, stock_location, place_of_origin,stock):
	dict_ = {
    "PRODUCTS": [
        {
            "SKU": sku,
            "NAME": name,
            "STOCK_LOCATION": stock_location,
            "PLACE_OF_ORIGIN": place_of_origin,
            "STOCK": stock,
        },
      
    ]
}

	out = open('app/data/data_'+sku+'.data', 'w+')
	json.dump(dict_, out, indent=4)
	out.close()

def dat(sku, name, stock_location, place_of_origin,stock,status, t_id):
	dict_ = {
    "PRODUCTS": [
        {
            "SKU": sku,
            "NAME": name,
            "STOCK_LOCATION": stock_location,
            "PLACE_OF_ORIGIN": place_of_origin,
            "STOCK": stock,
            "STATUS": status,
            "ID" : t_id
        },
      
    ]
}

	out = open('app/dat/data_'+str(i)+'.data', 'w+')
	json.dump(dict_, out, indent=4)
	out.close()


@app.route('/')
def home():
	if 'google_token' in session:
		me = google.get('userinfo')
		return render_template('home.html', title='Poha CMS', display='Poha', display1='Component Management System', login=str(me.data["name"]))
		#return jsonify({"data": me.data})
	return render_template('home.html', title='Poha CMS', display='Poha', display1='Component Management System', login="Login")

@app.route('/form', methods = ['GET', 'POST'])
def submit_form():
	sku_input = request.args.get('sku', None)
	quick = request.args.get('quick', None)
	form = product_submit()
	if request.method == 'POST':
			sku = request.form.get('sku', None)
			name = request.form.get('name', None)
			stock_location = request.form.get('stock_location', None)
			#place_of_origin = request.form.get('place_of_origin', None)
			qty = request.form.get('qty', None)
			data(sku, name, stock_location, "Not Issued", qty)
			flash('Saved')
			if 'google_token' in session:
				me = google.get('userinfo')
				return render_template('form.html', form=form, sku=sku, title=' ', display='Saved', display1=sku, extra=' ', login=str(me.data["name"]))
			return render_template('form.html', form=form, sku=sku, title=' ', display='Saved', display1=sku, extra=' ', login="Login")
		


	elif request.method == 'GET':
		if sku_input is None:
			return render_template('form.html', form=form, title='Product Input', display='New', display1='Product', extra=' ', sku_default=' ', name_default=' ',
				stock_default=' ', place_default=' ', qty_default=' ')
		elif sku_input is not None:
			

			if sku_input in open('app/data/data_'+sku_input+'.data').read() and quick is None:

				##DEFINE WH PRODUCTS

				a = open('app/data/data_'+sku_input+'.data')
				u = json.load(a)
							
				try:
					if u['PRODUCTS'][0]['SKU'] == sku_input:
						name = u['PRODUCTS'][0]['NAME']
						stock = u['PRODUCTS'][0]['STOCK_LOCATION']
						poo = u['PRODUCTS'][0]['PLACE_OF_ORIGIN']
						stock_qty = u['PRODUCTS'][0]['STOCK']
						if 'google_token' in session:
							me = google.get('userinfo')
							return render_template('form.html', form=form, title='Product Input', display='Edit', display1=sku_input, extra='', sku_default=sku_input, name_default=name,
						    stock_default=stock, place_default=poo, qty_default=stock_qty, login=str(me.data["name"]))
						return render_template('form.html', form=form, title='Product Input', display='Edit', display1=sku_input, extra='', sku_default=sku_input, name_default=name,
						stock_default=stock, place_default=poo, qty_default=stock_qty, login="Login")
				except u['PRODUCTS'][0]['SKU'] != sku_input:
						return 'NO ID FOUND'





@app.route('/quick', methods = ['GET', 'POST'])
def quick():
	global i
	sku_input = request.args.get('sku', None)
	form = product_submit()
	a = open('app/data/data_'+str(sku_input)+'.data')
	u = json.load(a)
	me = google.get('userinfo')
	if request.method == 'POST':
		q = request.form.get('qty', None)
		qty = int(u['PRODUCTS'][0]['STOCK']) - int(q)
		sku = u['PRODUCTS'][0]['SKU']
		name = u['PRODUCTS'][0]['NAME']
		stock = ""
		poo = str(me.data["name"])
		#data(sku, name, stock, company, poo, w, qty, product, u['PRODUCTS'][0]['STOCK'])
		data(sku, name, stock, poo, qty)
		i += 1
		dat(sku, name, stock, poo, q, 1,i)
		flash('Saved')

		if 'google_token' in session:
			me = google.get('userinfo')
			return render_template('quick.html', form=form, sku=sku, title=' ', display='Saved', display1=sku, extra=' ', sku_default=sku_input, name_default=name, qty_default=qty, login=str(me.data["name"]))
		return render_template('quick.html', form=form, sku=sku, title=' ', display='Saved', display1=sku, extra=' ', sku_default=sku_input, name_default=name, qty_default=qty, login="Login")

	elif request.method == 'GET':
		if sku_input in open('app/data/data_'+sku_input+'.data').read():
			a = open('app/data/data_'+sku_input+'.data')
			u = json.load(a)
								
			try:
				if u['PRODUCTS'][0]['SKU'] == sku_input:
					name = u['PRODUCTS'][0]['NAME']
					stock_qty = u['PRODUCTS'][0]['STOCK']
					return render_template('quick.html', form=form, title='Issue', display='', display1=sku_input, sku_default=sku_input, name_default=name,qty_default=stock_qty)

			except u['PRODUCTS'][0]['SKU'] != sku_input:
				return 'NO SKU FOUND'		

@app.route('/return', methods = ['GET', 'POST'])
def return1():
	global i
	sku_input_1 = request.args.get('sku', None)
	form_1 = product_submit()
	a_1 = open('app/data/data_'+str(sku_input_1)+'.data')
	u_1 = json.load(a_1)
	me_1 = google.get('userinfo')
	if request.method == 'POST':
		q_1 = request.form.get('qty', None)
		qty_1 = u_1['PRODUCTS'][0]['STOCK'] + int(q_1)
		sku_1 = u_1['PRODUCTS'][0]['SKU']
		name_1 = u_1['PRODUCTS'][0]['NAME']
		stock_location_1 = request.form.get('stock_location', None)
		#print(stock_location)
		poo_1 = str("Not Issued")
		#data(sku, name, stock, company, poo, w, qty, product, u['PRODUCTS'][0]['STOCK'])
		data(sku_1, name_1, stock_location_1, poo_1, qty_1)
		i += 1
		dat(sku_1, name_1, stock_location_1, poo_1, qty_1,2,i)
		flash('Saved')

		if 'google_token' in session:
			me = google.get('userinfo')
			return render_template('return.html', form=form_1, sku=sku_1, title=' ', display='', display1=sku_1, extra=' ', sku_default=sku_input_1, name_default=name_1, qty_default=qty_1,death=q_1, login=str(me_1.data["name"]))
		return render_template('return.html', form=form_1, sku=sku_1, title=' ', display='Saved', display1=sku_1, extra=' ', sku_default=sku_input_1, name_default=name_1, qty_default=qty_1, login="Login")

	elif request.method == 'GET':
		if sku_input_1 in open('app/data/data_'+sku_input_1+'.data').read():
			a_1 = open('app/data/data_'+sku_input_1+'.data')
			u_1 = json.load(a_1)
								
			try:
				if u_1['PRODUCTS'][0]['SKU'] == sku_input_1:
					name_1 = u_1['PRODUCTS'][0]['NAME']
					stock_qty_1 = u_1['PRODUCTS'][0]['STOCK']
					return render_template('return.html', form=form_1, title='Return', display='', display1=sku_input_1, sku_default=sku_input_1, name_default=name_1,qty_default=stock_qty_1, login=str(me_1.data["name"]))

			except u['PRODUCTS'][0]['SKU'] != sku_input:
				return 'NO ID FOUND'
			#else:
									


@app.route('/login')
def login():
	return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('home'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return redirect(url_for('home'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')	

@app.route('/all')
def view_products():
	product_path = 'app/data/'
	f = []
	location = []
	name_of_product = []
	qty = []
	skus = []
	place_of_origin=[]
	for (dirpath, dirnames, filenames) in os.walk(product_path):
		f.extend(filenames)
		break
	for dele in f:
		params = re.split('\W', dele)
		#company.append(params[1])
		#location.append(params[0])

	# Count the products
	all_products = len(f)



	for name_of in f:
		a = open('app/data/'+name_of)
		u = json.load(a)
		name = u['PRODUCTS'][0]['NAME']
		stock_qty = u['PRODUCTS'][0]['STOCK']
		sku = u['PRODUCTS'][0]['SKU']
		poo = u['PRODUCTS'][0]['PLACE_OF_ORIGIN']
		loc = u['PRODUCTS'][0]['STOCK_LOCATION']
		name_of_product.append(name)
		qty.append(stock_qty)
		skus.append(sku)
		place_of_origin.append(poo)
		location.append(loc)

	if 'google_token' in session:	
		me = google.get('userinfo')
		return render_template('all.html', title='Inventory', display='Inventory', 
		product=zip(name_of_product,qty, skus,location, place_of_origin), number_of_products=all_products, login=str(me.data["name"]))

	else:
		return render_template('all.html', title='Inventory', display='Inventory', 
		product=zip(name_of_product,qty, skus,location, place_of_origin), number_of_products=all_products, login="Login")	

@app.route('/hist')
def view_history():
	product_path = 'app/dat/'
	f=[]
	ids = []
	location = []
	name_of_product = []
	qty = []
	skus = []
	place_of_origin=[]
	status=[]
	for (dirpath, dirnames, filenames) in os.walk(product_path):
		f.extend(filenames)
		break
	for dele in f:
		params = re.split('\W', dele)
		#company.append(params[1])
		#location.append(params[0])

	# Count the products
	all_products = len(f)

	for name_of in f:
		a = open('app/dat/'+name_of)
		u = json.load(a)
		x = u['PRODUCTS'][0]['ID']
		name = u['PRODUCTS'][0]['NAME']
		stock_qty = u['PRODUCTS'][0]['STOCK']
		sku = u['PRODUCTS'][0]['SKU']
		poo = u['PRODUCTS'][0]['PLACE_OF_ORIGIN']
		loc = u['PRODUCTS'][0]['STOCK_LOCATION']
		stat =u['PRODUCTS'][0]['STATUS']
		ids.append(x)
		name_of_product.append(name)
		qty.append(stock_qty)
		skus.append(sku)
		place_of_origin.append(poo)
		location.append(loc)
		status.append(int(stat))

	if 'google_token' in session:	
		me = google.get('userinfo')
		return render_template('history.html', title='History', display='History', 
		product=zip(ids, name_of_product,qty, skus,location, place_of_origin, status), number_of_products=all_products, login=str(me.data["name"]))

	else:
		return render_template('history.html', title='History', display='History', 
		product=zip(ids, name_of_product,qty, skus,location, place_of_origin, status), number_of_products=all_products, login="Login")			

 

@app.route('/product/check', methods = ['GET', 'POST'])
def index():
	sku = request.args.get('sku', None)
	company_name = ' '
	location = ' ' 
	if sku is None:
		try:
			abort(400)
		except:
			return make_response(jsonify({'error':'wrong param'}))

	elif sku is not None:
		if sku in open('app/data/data_'+sku+'.data').read():

				##DEFINE WH PRODUCTS

			sku_origin = re.findall('\d+', sku)
			for i in sku_origin:
				pass
			a = open('app/data/data_'+sku+'.data')
			u = json.load(a)
						
			try:
				if u['PRODUCTS'][0]['SKU'] == sku:
					name = u['PRODUCTS'][0]['NAME']
					stock = u['PRODUCTS'][0]['STOCK_LOCATION']
					poo = u['PRODUCTS'][0]['PLACE_OF_ORIGIN']
					stock_qty = u['PRODUCTS'][0]['STOCK']

					if 'google_token' in session:	
						me = google.get('userinfo')
						return render_template('index.html', title=sku, display='Component Details', p_name=name, stock_location=stock, display1=poo, qty=stock_qty, login=str(me.data["name"]))

					else:
						return render_template('index.html', title=sku, display='Component Details', p_name=name, stock_location=stock, display1=poo, qty=stock_qty, login="Login")
					
			except u['PRODUCTS'][0]['SKU'] != sku:
					return 'NO ID FOUND'
						#return u['PRODUCTS'][0]['SKU']
						#return render_template('index.html', stat=sku, Company_Name=u[sku]['NAME'], product='http://sysbase.org/check/images/'+i)

		else:
			return 'Could not find ID'

@app.route('/stat')
def stats():
	places = []
	f = []
	places_count = {}
	getPlaces = []
	location = []
	skus = []
	qty = []
	orig_qty = []
	product_path = 'app/data/'
	#Get all unique places
	for (dirpath, dirname, filnames) in os.walk(product_path):
		f.extend(filnames)
		for ii in filnames:
			print(ii)
			i = open(product_path+ii)
			u=json.load(i)
			skus.append(str(u['PRODUCTS'][0]['SKU']))
			places.append(u['PRODUCTS'][0]['PLACE_OF_ORIGIN'])
			qty.append(int(u['PRODUCTS'][0]['STOCK']))
			i.close()
	for dele in f:
		params = re.split('\W', dele)
		location.append(params[0])
	for place in places:
		if place not in getPlaces:
			getPlaces.append(place)

	for o in getPlaces:
		places_count[o] = places.count(o)

	all_products = len(f)

	return render_template('stat.html', title='Stats', display='Analytics', number_of_products=all_products, 
		places=places_count, sku=str(skus), qty=str(qty))





    