from marshmallow import Schema, validate, fields
from datetime import date
import enum
class CreateUser(Schema):
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String(validate=validate.Email())
    password = fields.String()
    phone = fields.Function(validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$'))
    status = fields.String(validate=validate.OneOf(["paid", "did_not_pay", "the_credit_is_still_valid"]), default="paid")


class UpdateUser(Schema):
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String(validate=validate.Email())
    password = fields.String()
    phone = fields.Function(validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$'))

class CreateCredit(Schema):
    sum_of_credit = fields.Float()
    percent_of_credit = fields.Float()
    user_id = fields.Integer()
    creditor_id = fields.Integer()
    register_at = fields.Date(validate=lambda x: x == date.today())
    deadline = fields.Date(validate=lambda x: x > date.today())
    status = fields.String(validate=validate.OneOf(["paid", "did_not_pay", "the_credit_is_still_valid"]),
                           default="paid")


class UpdateCredit(Schema):
    sum_of_credit = fields.Float()
    status = fields.String(validate=validate.OneOf(["paid", "did not pay", "the credit is still valid"]),
                           default="paid")
    percent_of_credit = fields.Float()

class CreateCreditor(Schema):
    name = fields.String()
    phone = fields.Function(validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$'))
    budget = fields.Float(validate=lambda x: x <= 517000)


class UpdateCreditor(Schema):
    name = fields.String()
    phone = fields.Function(validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$'))
    budget = fields.Float(validate=lambda x: x <= 517000)