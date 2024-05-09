from string import Template
from textwrap import dedent

wsgi_template = Template(
    dedent(
        """\
    from ${app_name} import create_app

    app = create_app()

    if __name__ == '__main__':
        app.run()
    """
    )
)

procfile_template = Template(
    dedent(
        """\
    web: gunicorn wsgi:app

    """
    )
)

tests_template = Template(
    dedent(
        """\
    import unittest

    # write your tests here
    """
    )
)

app_init_template = Template(
    dedent(
        """\
        import logging
        import os
        from logging.handlers import RotatingFileHandler
        from flask import Flask
        from config import Config, Development

        def get_env_config():
            # Retrieve environment-specific config class based on environment variables.
            env = os.getenv('APP_ENV', os.getenv('FLASK_ENV'))
            if env == 'dev':
                return Development
            elif env == 'prod':
                return Config
            raise EnvironmentError(
                "No APP_ENV or FLASK_ENV is set! Please set one to 'dev' or 'prod'."
            )

        def configure_logging(app):
            # Configure the app's logging.
            if app.debug or app.testing:
                if app.config.get('LOG_TO_STDOUT'):
                    stream_handler = logging.StreamHandler()
                    stream_handler.setLevel(logging.INFO)
                    app.logger.addHandler(stream_handler)
                else:
                    log_dir = 'logs'
                    os.makedirs(log_dir, exist_ok=True)
                    file_handler = RotatingFileHandler(
                        os.path.join(log_dir, f'{app.config["APP_NAME"]}.log'),
                        maxBytes=20480,
                        backupCount=20,
                    )
                    file_handler.setFormatter(
                        logging.Formatter(
                            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
                        )
                    )
                    file_handler.setLevel(logging.INFO)
                    app.logger.addHandler(file_handler)
                app.logger.setLevel(logging.INFO)
                app.logger.info(f'{app.config["APP_NAME"]} startup')

        def create_app():
            # Construct the core application.
            app = Flask(__name__, instance_relative_config=False)
            app.config.from_object(get_env_config())

            with app.app_context():
                # Register API blueprint
                from ${app_name}.${main_bp_name} import ${main_bp_name}
                app.register_blueprint(${main_bp_name}, url_prefix='/')

                # Configure logging
                configure_logging(app)

            return app
        """
    )
)

main_bp_routes_template = Template(
    dedent(
        """\
    from datetime import datetime
    from ${app_name}.${main_bp_name} import ${main_bp_name}
    from flask import jsonify, render_template

    @${main_bp_name}.route('/api')
    def api():
        data = {
            'message': 'Hello world!',
            'timestamp': datetime.utcnow()
        }
        return jsonify(data), 200

    @${main_bp_name}.route('/')
    def index():
        return render_template('index.html')

    """
    )
)

main_bp_init_template = Template(
    dedent(
        """\
    from flask import Blueprint

    ${main_bp_name} = Blueprint('${main_bp_name}', __name__)
    from ${app_name}.${main_bp_name} import routes

    """
    )
)

requirements_template = Template(
    dedent(
        """\
    flask>=3.0.0
    gunicorn
    """
    )
)

config_template = Template(
    dedent(
        """\
    import os

    basedir = os.path.abspath(os.path.dirname(__file__))

    class Config(object):
        '''Environment variabbles'''

        PROJECT_NAME = '${project_name}'
        APP_NAME = '${app_name}'
        APP_RUNTIME = '${runtime}'
        APP_DESCRIPTION = '${description}'

        APP_ENV = os.environ.get('APP_ENV') or 'prod'
        FLASK_ENV = os.environ.get('APP_ENV') or 'prod'
        TESTING = os.environ.get('TESTING') or False
        DEBUG = os.environ.get('DEBUG') or False

        LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or False
        SECRET_KEY = os.environ.get('SECRET_KEY') or b'your_secrete_key'

    class Development(Config):
        '''Environment variabbles'''
        
        APP_ENV = os.environ.get('APP_ENV') or 'dev'
        FLASK_ENV = os.environ.get('APP_ENV') or 'dev'
        TESTING = os.environ.get('TESTING') or False
        DEBUG = os.environ.get('DEBUG') or True

        LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or True
        SECRET_KEY = os.environ.get('SECRET_KEY') or b'your_secrete_key'

    """
    )
)

runtime_template = Template(
    dedent(
        """\
    python-${runtime}
    """
    )
)

html_index = Template(
    dedent(
        """\
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>${project_name}</title>
            <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css', _external=True) }}">
        </head>
        <body>
            <div class="container">
                <h1>${project_name}</h1>
                <p>${description}</p>
                
                <section>
                    <h2>API Endpoints:</h2>
                    <ul>
                        <li><a href="/api">/api</a></li>
                    </ul>
                </section>

                <p>
                    <a href="https://github.com/MurphyAdam/kickstart-flask-app"
                        alt="GitHub repository for kickstart-flask-app package">View on GitHub
                    </a>
                </p>
            </div>
        </body>
        </html>
    """
    )
)

style_css = Template(
    dedent(
        """\
        html,
        body {
            height: 100%;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
            font-size: 16px;
            background: #fafafa;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            text-align: center;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            width: 90%;
            max-width: 600px;
            background: #fff;
            border-radius: 8px;
        }

        h1,
        h2 {
            color: #4db6ac;
            margin: 0 0 20px 0;
        }

        h2 {
            font-size: 1.4rem;
        }

        p,
        ul {
            font-size: 1.2rem;
            line-height: 1.6;
            margin: 10px 0;
        }

        ul {
            list-style-type: none;
            padding: 0;
            margin: 0 0 20px 0;
            text-align: center;
        }

        li {
            padding: 8px 0;
            border-bottom: 1px solid #ccc;
        }

        li:last-child {
            border-bottom: none;
        }

        a {
            color: #4db6ac;
            text-decoration: none;
            font-size: 1rem;
            font-weight: bold;
        }

        a:hover {
            text-decoration: underline;
        }
    """
    )
)
