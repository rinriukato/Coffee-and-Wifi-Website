from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

COFFEE_RATING = ['✘', '☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕']
WIFI_RATING = ['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪']
POWER_RATING = ['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌']


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label='Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL(message="Invalid URL")])
    open = StringField(label='Opening Time e.g. 8AM', validators=[DataRequired()])
    close = StringField(label='Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee = SelectField(label='Coffee Rating', choices=COFFEE_RATING, validators=[DataRequired()])
    wifi = SelectField(label='Wifi Strength Rating', choices=WIFI_RATING, validators=[DataRequired()])
    power = SelectField(label='Power Socket Availability', choices=POWER_RATING, validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print(form.cafe.data)
        new_cafe_entry = [form.cafe.data, form.location.data, form.open.data, form.close.data, form.coffee.data,
                          form.wifi.data, form.power.data]
        with open('cafe-data.csv', 'a', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(new_cafe_entry)

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
