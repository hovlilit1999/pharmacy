from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drug.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comp_name = db.Column(db.String(100), nullable=False)
    comp_country = db.Column(db.String(100), nullable=False)
    comp_description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Company %r>' % self.id


class Drug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drug_name = db.Column(db.String(100), nullable=False)
    drug_company = db.Column(db.String(100), nullable=False)
    drug_description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Drug %r>' % self.id


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/create_company", methods=['POST', 'GET'])
def create_company():
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_country = request.form['company_country']
        description = request.form['description']

        new_company = Company(comp_name=company_name, comp_country=company_country, comp_description=description)

        try:
            db.session.add(new_company)
            db.session.commit()
            return redirect('/all_companies')
        except:
            return 'Can\'t add company'
    else:
        return render_template("create_company.html")


@app.route("/create_drug", methods=['POST', 'GET'])
def create_drug():
    if request.method == 'POST':
        drug_name = request.form['drug_name']
        drug_company = request.form['drug_company']
        description = request.form['description']

        new_drug = Drug(drug_name=drug_name, drug_company=drug_company, drug_description=description)

        try:
            db.session.add(new_drug)
            db.session.commit()
            return redirect('/all_drugs')
        except:
            return 'Can\'t create drug'
    else:
        return render_template("create_drug.html")


@app.route("/all_companies", methods=['POST', 'GET'])
def company():
    companies = Company.query.order_by(Company.comp_name).all()
    return render_template("all_companies.html", companies=companies)


@app.route("/all_companies/<int:id>", methods=['POST', 'GET'])
def company_detail(id):
    my_company = Company.query.get(id)
    return render_template("company_detail.html", my_company=my_company)


@app.route("/all_companies/<int:id>/delete", methods=['POST', 'GET'])
def company_delete(id):
    my_company = Company.query.get_or_404(id)

    try:
        db.session.delete(my_company)
        db.session.commit()
        return redirect('/all_companies')
    except:
        return "can\'t delete company"


@app.route("/all_companies/<int:id>/update_company", methods=['POST', 'GET'])
def update_company(id):
    my_company = Company.query.get(id)
    if request.method == 'POST':
        my_company.company_name = request.form['company_name']
        my_company.company_country = request.form['company_country']
        my_company.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/all_companies')
        except:
            return 'Can\'t update company'
    else:
        return render_template("update_company.html", my_company=my_company)


@app.route("/all_drugs", methods=['POST', 'GET'])
def drug():
    drugs = Drug.query.order_by(Drug.drug_name).all()
    return render_template("all_drugs.html", drugs=drugs)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
