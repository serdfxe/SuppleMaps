from app import create_app
from waitress import serve

app = create_app()

if __name__ == "__main__":
    #serve(app, host='0.0.0.0')
    app.run("127.0.0.1", port=80)