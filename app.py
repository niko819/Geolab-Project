from ext import app

if __name__ == "__main__":
    from routes import home, register, login, about, second, playstation, User, create_product, edit_product, delete_product, submit_contact, thank_you

app.run(debug=True)
