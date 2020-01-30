from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class product_submit(Form):
    sku = StringField('sku', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    stock_location = StringField('stock_location', validators=[DataRequired()])
    place_of_origin = StringField('place_of_origin', validators=[DataRequired()])
    qty = StringField('qty', validators=[DataRequired()])
