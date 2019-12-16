from flask import render_template
from frontend import app
from frontend.forms import IRForm, ResForm
import frontend.util as util

@app.route('/', methods=['GET', 'POST'])
def main():
    form = IRForm()
    result = ResForm()

    if form.validate_on_submit():
        util.query(form, result)
    return render_template('ir.html', form=form, result=result)

