from wtforms import Form, StringField, SubmitField


class ProjectForm(Form):
    title = StringField()
    description = StringField()
