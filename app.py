from service import create_app

# app = Flask(__name__)
#
#
# if __name__ == "__main__":
#     # port = int(os.environ.get('PORT', 5000))
#     openai_key = os.getenv("OPENAI_API_KEY")
#
#     app.run(debug=True, port=5005)


app = create_app()

if __name__ == "__main__":
    app.run(port=5000)
