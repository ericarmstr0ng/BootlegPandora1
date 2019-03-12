import os

from flask import Flask
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
			SECRET_KEY='dev',
			SESSION_TYPE='filesystem'
		)

	return app


class InfoForm(FlaskForm):
	artist = StringField('Artist')
	submit = SubmitField('Submit')
