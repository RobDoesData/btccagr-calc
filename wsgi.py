
from app.main import app
  
if __name__ == "__main__":
        app.jinja_env.auto_reload = True
        app.static_folder = 'static'
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run()
