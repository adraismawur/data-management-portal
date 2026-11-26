from wtforms import Form, StringField


class TestLoginForm(Form):
    user_name = StringField()
