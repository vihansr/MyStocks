from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

app = Flask(__name__)
Bootstrap5(app)
app.config['SECRET_KEY'] = 'buyvoy87v8O&VOY^CY(&TX^*XRCYTVYBIUPBV'

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analysis.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class StockForm(FlaskForm):
    stock = StringField('Enter Stock Name', validators=[DataRequired()])
    heading = StringField('Enter Heading for Analysis', validators=[DataRequired()])
    analysis = StringField('Give your Analysis', validators=[DataRequired()])
    submit = SubmitField('Add Analysis', render_kw={'class': 'btn btn-success'})

class Analysis(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock: Mapped[str] = mapped_column(String(50), nullable=False)
    heading: Mapped[str] = mapped_column(String(100), nullable=False)
    analysis: Mapped[str] = mapped_column(String(1000), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    result = db.session.execute(db.select(Analysis))
    posts = result.scalars().all()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = StockForm()
    if form.validate_on_submit():
        new_analysis = Analysis(
            stock=form.stock.data,
            analysis=form.analysis.data,
            heading=form.heading.data,
            date=datetime.now().strftime('%Y-%m-%d')
        )

        db.session.add(new_analysis)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/delete')
def delete():
    post_id = request.args.get('id')
    post_to_delete = db.get_or_404(Analysis, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:post_id>', methods=['GET','POST'])
def edit(post_id):
    post = db.get_or_404(Analysis, post_id)

    edit_form = StockForm(
        stock= post.stock,
        analysis= post.analysis,
        heading= post.heading,
    )

    if edit_form.validate_on_submit():
        post.stock = edit_form.stock.data
        post.analysis = edit_form.analysis.data
        post.heading = edit_form.heading.data
        db.session.commit()
        return redirect(url_for("index"))
    return render_template('add.html', form= edit_form)

if __name__ == '__main__':
    app.run(debug=True)
