import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    
  @staticmethod
  def init_app(app):
    pass


class DevelopmentConfig(Config):
  DEBUG = True

class TestingConfig(Config):
  TESTING = True

# class ProductionConfig(Config):
  #

config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,

  'default': DevelopmentConfig
}