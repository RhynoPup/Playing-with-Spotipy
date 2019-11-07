config = {
    "development": "soundstyles.config.DevelopmentConfig",
    "testing": "soundstyles.config.TestingConfig",
    "default": "soundstyles.config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name]) # object-based default configuration
    app.config.from_pyfile('config.cfg', silent=True) # instance-folders configuration