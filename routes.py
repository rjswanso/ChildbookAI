from app import f_app, db
from funcs import create_Story, getImagesFromAI
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from datetime import datetime
from models import Story
import forms
import json

@f_app.route('/')
@f_app.route('/index')
def index():
    stories = get_results_from_db(Story)
    return render_template('index.html', stories=stories)

@f_app.route('/add', methods=['Get', 'Post'])
def add():
    form = forms.AddStoryForm()
    if form.validate_on_submit():
        story_sentences = []
        characters = form.characters.data
        story_prompt = form.story_prompt.data
        story_title, story_plot, story_sections, story_section_chunks = create_Story(characters, story_prompt)
        new_story = Story(title=story_title, story_synopsis=story_plot, story_section_titles=json.dumps(story_sections), story_section_chunks=json.dumps(story_section_chunks), date=datetime.utcnow())
        add_results_to_db(db, new_story)
        flash('Story added to database')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@f_app.route('/about', methods=['Get', 'Post'])
def about():
    return render_template('about.html')

@f_app.route('/delete/<int:story_id>', methods=['Get', 'Post'])
def delete(story_id):
    story = Story.query.get(story_id)
    form = forms.DeleteStoryForm()
    if story:
        if form.validate_on_submit():
            db.session.delete(story)
            db.session.commit()
            flash('Story has been deleted')
            return redirect(url_for('index'))
    else:
        flash('Story not found') 
        return redirect(url_for('index'))
    return render_template('delete.html', form=form, story_id=story_id, title=story.title)

### Include a story editor ###

@f_app.route('/edit/<int:story_id>', methods=['Get', 'Post'])
def edit(story_id):
    story = Story.query.get(story_id)
    form = forms.EditTitleForm()

    if story:
        if form.validate_on_submit():
            story.title = form.title.data
            story.date = datetime.utcnow()
            db.session.commit()
            flash('Story has been updated as: ' + story.title)
            return redirect(url_for('index'))
        form.title.data = story.title
        return render_template('edit.html',form=form, story_id=story_id, story=story)
    else:
        flash('Story not found') 
    return redirect(url_for('index'))

@f_app.route('/viewstory/<int:story_id>', methods=['Get', 'Post'])
def viewstory(story_id):
    img_urls = []
    story = Story.query.get(story_id)
    form = forms.AddImagestoStory()
    len_sections = len(json.loads(story.story_section_titles))
    if story:
        if form.validate_on_submit():
            style = form.style.data
            img_urls = getImagesFromAI(story,style)
            flash('image created')
            print(img_urls)
            return redirect(url_for('viewstory', story_id=story_id))
            #add images from AI pull
    else:
        flash('Story not found') 
        return redirect(url_for('index'))
    return render_template('viewstory.html', form=form, story_id=story_id, title=story.title, sections=json.loads(story.story_section_titles), section_chunks=json.loads(story.story_section_chunks), len_sections=len_sections, img_urls=img_urls)

""" Don't think this is needed
@f_app.route('viewstoryimages/<int:story_id>', methods=['Get','Post'])
def viewstoryimages(story_id):
    story = Story.query.get(story_id)
    form = forms.MakeStoryBook()

    if story:
        if form.validate_on_submit:
            return render_template('makestorybook.html',story_id=story_id)
"""

"""
@f_app.route('/makestorybook/<int:story_id>',methods=['Get','Post'])
def makestorybook(story_id,images):
    story = story = Story.query.get(story_id)

"""
def add_results_to_db(db, result):
    db.session.add(result)
    db.session.commit()

def get_results_from_db(className):
    #with app.app_context():
    items = className.query.all()
    return items
