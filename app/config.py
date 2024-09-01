import os 
from decouple import config

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	CSRF_ENABLED = True

	SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')
