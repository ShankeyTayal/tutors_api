from werkzeug.serving import run_simple
from bootstrap.app import create_app


app = create_app()


if __name__ == '__main__':
    # Run Server
    run_simple(
        '0.0.0.0', 5000, app, use_reloader=True,
        use_debugger=True, use_evalex=True
    )
