from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired

class AddStoryForm(FlaskForm):
    title = StringField('Title')
    characters = StringField('Character names?', validators=[DataRequired()])
    story_prompt = TextAreaField('What do you want your story to be about?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditTitleForm(FlaskForm):
    title = StringField('Edit Title', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteStoryForm(FlaskForm):
    submit = SubmitField('Delete Story')

class AddImagestoStory(FlaskForm):
    style = StringField('Would you like the images in any particular style?')
    submit = SubmitField('Add Images')

class MakeStoryBook(FlaskForm):
    submit = SubmitField('Make StoryBook')    