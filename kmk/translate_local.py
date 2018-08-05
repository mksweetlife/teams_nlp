from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from translate_test import translate_function
import kmk0805

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

# sim = 0

class NameForm(FlaskForm):
    name = StringField('영단어를 입력하세요:', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    Trans = None
    Rom = None
    Sim = None 
    Result2 = None
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        Trans = translate_function(name)[0]
        Rom = translate_function(name)[1]
        Sim = kmk0805.similar(name)
        Result1 = sim.MarkovName(name)
        Result2 = result1.generate_name(name)

        #form.name.data = ''
    return render_template('index.html', form=form, name1=Trans, name2=Rom, name3=Sim, name4=Result2) ##



if __name__ == '__main__':
    app.run(debug=True)
