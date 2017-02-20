from wtforms import Form, StringField, validators

class RegistrationForm(Form):
    username = StringField('username', [validators.Length(min=0, max=128)])
    day = StringField('day', [validators.Length(min=0, max=128)])
    month = StringField('month', [validators.Length(min=0, max=128)])
    year = StringField('year', [validators.Length(min=0, max=128)])
    domain_name = StringField('domain_name', [validators.Length(min=0, max=128)])
