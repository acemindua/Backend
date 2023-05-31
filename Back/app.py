import enum
from datetime import date, datetime


from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dateutil.relativedelta import relativedelta
from flask_bcrypt import bcrypt
from flask_bcrypt import generate_password_hash
from flask_bcrypt import check_password_hash

app = Flask(__name__)
cors = CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

db = SQLAlchemy(app)


class StatusField(enum.Enum):
    paid = 'paid'
    did_not_pay = 'did not pay'
    the_credit_is_still_valid = 'the credit is still valid'

    def __repr__(self):
        return '%r' % self.value

    def __str__(self):
        return self.value

    def __name__(self):
        return self.value


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.Enum(StatusField), nullable=False)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def __repr__(self):
        return '<User %r %r>' % (self.first_name, self.last_name)


class Credit(db.Model):
    credit_id = db.Column(db.Integer, primary_key=True)
    sum_of_credit = db.Column(db.Numeric, nullable=False)
    percent_of_credit = db.Column(db.Numeric, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    creditor_id = db.Column(db.Integer, nullable=False)
    register_at = db.Column(db.Date, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(StatusField), nullable=False)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def __repr__(self):
        return '<Credit %r>' % self.credit_id


class Creditor(db.Model):
    creditor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, unique=True, nullable=False)
    budget = db.Column(db.Numeric, nullable=False)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def __repr__(self):
        return '<Creditor %r>' % self.name


class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    credit_id = db.Column(db.Numeric, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def __repr__(self):
        return '<Creditor %r>' % self.name


class Error(db.Model):
    code = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


def fill_user_data(user_data, user=None):
    error_message = ''
    first_name = ''
    last_name = ''
    password = ''
    email = ''
    phone = ''
    status = ''
    if user_data:
        if 'first_name' in user_data:
            first_name = user_data['first_name']
        elif not user:
            error_message += 'Fist Name is emtpy.\n'
        if 'last_name' in user_data:
            last_name = user_data['last_name']
        elif not user:
            error_message += 'Last Name is emtpy.\n'
        if 'status' in user_data:
            status = user_data['status']
        elif not user:
            error_message += 'Status is emtpy.\n'
        if 'email' in user_data:
            email = user_data['email']
        if 'phone' in user_data:
            phone = user_data['phone']
        if 'password' in user_data:
            password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
        elif not user:
            error_message += 'Password is emtpy.\n'
    if not user:
        user = User()

    user.first_name = first_name if first_name else user.first_name
    user.last_name = last_name if last_name else user.last_name
    user.password = password if password else user.password
    user.email = email if email else user.email
    user.phone = phone if phone else user.phone
    user.status = status if status else user.status

    return user, error_message


def fill_credit_data(credit_data, credit=None):
    error_message = ''
    sum_of_credit = ''
    percent_of_credit = 0.05
    user_id = ''
    creditor_id = ''
    register_at = date.today()
    deadline = register_at + relativedelta(months=3)
    status = ''

    if credit_data:
        if 'sum_of_credit' in credit_data:
            sum_of_credit = credit_data['sum_of_credit']
        elif not credit:
            error_message += 'Sum of credit should be defined.\n'
        if 'user_id' in credit_data:
            user_id = credit_data['user_id']
        elif not credit:
            error_message += 'User should be defined.\n'
        if 'creditor_id' in credit_data:
            creditor_id = credit_data['creditor_id']
        elif not credit:
            error_message += 'Creditor should be defined.\n'
        if 'status' in credit_data:
            status = credit_data['status']
        elif not credit:
            error_message += 'Status is emtpy.\n'
        if 'percent_of_credit' in credit_data:
            percent_of_credit = credit_data['percent_of_credit']
        if 'register_at' in credit_data:
            register_at = datetime.strptime(credit_data['register_at'], '%d%m%Y').date()
        if 'deadline' in credit_data:
            deadline = datetime.strptime(credit_data['deadline'], '%d%m%Y').date()

    if not credit:
        credit = Credit()

    credit.sum_of_credit = sum_of_credit if sum_of_credit else credit.sum_of_credit
    credit.user_id = user_id if user_id else credit.user_id
    credit.creditor_id = creditor_id if creditor_id else credit.creditor_id
    credit.status = status if status else credit.status
    credit.percent_of_credit = percent_of_credit if percent_of_credit else credit.percent_of_credit
    credit.register_at = register_at if register_at else credit.register_at
    credit.deadline = deadline if deadline else credit.deadline

    return credit, error_message


def fill_creditor_data(creditor_data, creditor=None):
    error_message = ''
    name = ''
    budget = 0
    phone = ''

    if creditor_data:
        if 'name' in creditor_data:
            name = creditor_data['name']
        elif not creditor:
            error_message += 'Name be defined.\n'
        if 'budget' in creditor_data:
            budget = creditor_data['budget']
        elif not creditor:
            error_message += 'Budget should be defined.\n'

        if 'phone' in creditor_data:
            phone = creditor_data['phone']

    if not creditor:
        creditor = Creditor()

    creditor.name = name if name else creditor.name
    creditor.budget = budget if budget else creditor.budget
    creditor.phone = phone if phone else creditor.phone

    return creditor, error_message


def fill_payment_data(payment_data):
    error_message = ''
    user_id = ''
    amount = 0
    credit_id = ''

    if payment_data:
        if 'user_id' in payment_data:
            user_id = payment_data['user_id']
        else:
            error_message += 'Name be defined.\n'
        if 'amount' in payment_data:
            amount = payment_data['amount']
        else:
            error_message += 'Budget should be defined.\n'

        if 'credit_id' in payment_data:
            credit_id = payment_data['credit_id']
        else:
            error_message += 'Budget should be defined.\n'
    payment = Payment(
        user_id=user_id,
        amount=amount,
        credit_id=credit_id,
        date=date.today()
    )

    return payment, error_message


@app.route('/api/v1/user', methods=['POST'])
def create_user():  # put application's code here
    user_data = request.get_json()
    new_user, error_message = fill_user_data(user_data)
    if not error_message:
        db.session.add(new_user)
        db.session.commit()
        return new_user.as_dict()
    else:
        return Error(message=error_message).as_dict()

@app.route('/api/v1/user/login', methods=['POST'])
def login():
    email = request.get_json()
    password = request.get_json()
    if not email:
        return 'Email is emtpy.', 400
    if not password:
        return 'Password is emtpy.', 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return "User not found", 404

    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        return f'Logged in, Welcome {email}!', 200
    else:
        return 'Invalid Login Info!', 400


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return [user.as_dict() for user in User.query.all()]


@app.route('/api/v1/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_actions(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return "Record not found", 404

    if request.method == 'GET':
        return user.as_dict()
    elif request.method == 'PUT':
        user_data = request.get_json()
        new_user, error_message = fill_user_data(user_data, user)

        if error_message:
            return error_message, 400

        db.session.commit()
        return user.as_dict()
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return 'User deleted'


@app.route('/api/v1/user/findByStatus', methods=['GET'])
def find_user_by_status():
    try:
        status = StatusField(request.args.get('status'))
        return [user.as_dict() for user in User.query.filter_by(status=status.value)]
    except Exception as e:
        print(e)
        return 'Bad status', 400


@app.route('/api/v1/user/findByName', methods=['GET'])
def find_user_by_name():
    try:
        first_name = request.args.get('firstName')
        last_name = request.args.get('lastName')

        if not first_name:
            return 'Fist Name is emtpy.', 400
        if not last_name:
            return 'Last Name is emtpy.', 400

        return [user.as_dict() for user in
                User.query.filter(User.first_name == first_name and User.last_name == last_name)]
    except Exception as e:
        print(e)
        return 'Bad request', 400


@app.route('/api/v1/credit', methods=['POST'])
def create_credit():  # put application's code here
    credit_data = request.get_json()
    new_credit, error_message = fill_credit_data(credit_data)
    if not error_message:
        db.session.add(new_credit)
        db.session.commit()
        return new_credit.as_dict()
    else:
        return Error(message=error_message).as_dict()


@app.route('/api/v1/credits', methods=['GET'])
def get_credits():
    return [credit.as_dict() for credit in Credit.query.all()]


@app.route('/api/v1/credit/<credit_id>', methods=['GET', 'PUT', 'DELETE'])
def credit_actions(credit_id):
    credit = Credit.query.filter_by(credit_id=credit_id).first()
    if not credit:
        return "Record not found", 404

    if request.method == 'GET':
        return credit.as_dict()
    elif request.method == 'PUT':
        credit_data = request.get_json()
        credit, error_message = fill_credit_data(credit_data, credit)

        if error_message:
            return error_message, 400

        db.session.commit()
        return credit.as_dict()
    elif request.method == 'DELETE':
        db.session.delete(credit)
        db.session.commit()
        return 'Credit deleted'


@app.route('/api/v1/credit/findByStatus', methods=['GET'])
def find_credit_by_status():
    try:
        status = StatusField(request.args.get('status'))
        return [credit.as_dict() for credit in Credit.query.filter_by(status=status.value)]
    except Exception as e:
        print(e)
        return 'Bad status', 400


@app.route('/api/v1/credit/findByRegisterDate', methods=['GET'])
def find_credit_by_register_date():
    try:
        register_date = datetime.strptime(request.args.get('registerDate'), '%d%m%Y').date()
        return [credit.as_dict() for credit in Credit.query.filter_by(register_date=register_date)]
    except Exception as e:
        print(e)
        return 'Bad status', 400


@app.route('/api/v1/creditor', methods=['POST'])
def create_creditor():  # put application's code here
    creditor_data = request.get_json()
    new_creditor, error_message = fill_creditor_data(creditor_data)
    if not error_message:
        db.session.add(new_creditor)
        db.session.commit()
        return new_creditor.as_dict()
    else:
        return Error(message=error_message).as_dict()


@app.route('/api/v1/creditors', methods=['GET'])
def get_creditors():
    return [creditor.as_dict() for creditor in Creditor.query.all()]


@app.route('/api/v1/creditor/<creditor_id>', methods=['GET', 'PUT', 'DELETE'])
def creditor_actions(creditor_id):
    creditor = Creditor.query.filter_by(creditor_id=creditor_id).first()
    if not creditor:
        return "Record not found", 404

    if request.method == 'GET':
        return creditor.as_dict()
    elif request.method == 'PUT':
        creditor_data = request.get_json()
        creditor, error_message = fill_creditor_data(creditor_data, creditor)

        if error_message:
            return error_message, 400

        db.session.commit()
        return creditor.as_dict()
    elif request.method == 'DELETE':
        db.session.delete(creditor)
        db.session.commit()
        return 'Creditor deleted'


@app.route('/api/v1/credit/pay', methods=['POST'])
def pay_credit():  # put application's code here
    payment_data = request.get_json()
    new_payment, error_message = fill_payment_data(payment_data)
    if not error_message:
        db.session.add(new_payment)
        credit = Credit.query.filter_by(credit_id=new_payment.credit_id).first()
        if not credit:
            return 'Credit is not valid', 404
        if credit.register_at == new_payment.date:
            credit.sum_of_credit -= new_payment.amount
        else:
            credit.sum_of_credit += (credit.sum_of_credit * credit.percent_of_credit) \
                                    / 12 * relativedelta(date.today(), credit.register_at).months
            credit.sum_of_credit -= new_payment.amount
        if credit.sum_of_credit <= 0:
            credit.status = StatusField.paid
        db.session.commit()
        return new_payment.as_dict()
    else:
        return Error(message=error_message).as_dict()


if __name__ == '__main__':
    app.run()
    db.drop_all()
    db.create_all()
