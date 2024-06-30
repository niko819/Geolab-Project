from flask import render_template, redirect, flash
from forms import RegisterForm, LoginForm, ProductForm, ContactForm
from models import Product, User, ContactMessage
from os import path
from ext import app, db
from flask_login import login_user, logout_user, login_required, current_user

profiles = []
profile = []

product = []

ragacas = [{"name": "Samsung TV QE55S90CAUXRU OLED (2023)", "price": 4200,
            'img': "https://alta.ge/images/thumbnails/900/650/detailed/287/1_5afm-n2_5sw3-qp.png.jpg", "id":0 },
           {"name": "Samsung S928B Galaxy S24 Ultra (12GB/1TB) LTE/5G Dual Sim - Gray", "price": 5000,
            "img": "https://alta.ge/images/thumbnails/900/650/detailed/314/148689_1_61gq-cr_nshf-8v.png.jpg", "id":1},
           {"name": "Asus ROG Flow Z13 (2022) 2-in-1 Gaming Laptop (GZ301ZE-LD225W) - Black", "price": 4500,
            "img": "https://alta.ge/images/thumbnails/900/650/detailed/248/129031.png.jpg", "id":2},
           {"name": "Genesis Cobalt 330 4-In-1 Gaming Combo", "price": 150,
            "img": "https://alta.ge/images/thumbnails/900/650/detailed/210/qzjegjwerdyz67b74syqf93i.png.jpg", "id":3},
           {"name": "Philips EP1224/00", "price": 1200,
            "img": "https://alta.ge/images/thumbnails/900/650/detailed/306/1_gq7k-hr.png.jpg", "id":4},
           {"name": "Franko FGT-1146", "price": 250,
            "img": "https://alta.ge/images/thumbnails/900/650/detailed/329/94975.png.jpg", "id":5}]

playstations = [{"name": "WWE2k24", "price": 353,
                 "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2F35a0c18f-4699-4fa5-b2a1-286adebf4fab_Thumb.jpeg&w=384&q=100", "id":0},
                {"name": "Assassins Creed Mirage Game for PS5", "price": 333,
                 "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2Fdbb06318-8d9c-4089-ae15-f315f1ea829d_Thumb.jpeg&w=384&q=100", "id":1},
                {"name": "NBA 2K24 Game for PS5", "price": 120,
                 "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2F0f3fdf9c-c9d7-4146-875f-af6c6ca9e2d8_Thumb.jpeg&w=384&q=100", "id":2},
                {"name": "Sony PlayStation PS5 Slim 1TB Digital Edition", "price": 1500,
                 "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2F5ef7efe5-91e8-466a-9217-ae02425583ab_Thumb.jpeg&w=384&q=100", "id":3},
                {"name": "PS5 Wireless Controller Dualsense White", "price": 150,
                 "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fzoommer-images%2Fthumbs%2F0140867_ps5-wireless-controller-dualsense-white_550.jpeg&w=384&q=100", "id":4},
                {"name": "Sony Playstation PS5 DualSense Charging Station White", "price": 99,
                 "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2F168d70eb-ddd8-48f5-a1fd-a5dd5862a366_Thumb.jpeg&w=384&q=100", "id":5}]

televisions = [{"name": "Samsung TV UE85CU8072UXXH-2023-ტელევიზორი", "price": 5000,
                "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2F2a0d4b3e-e5e8-48d5-8ce0-37fabb893b0f_Thumb.jpeg&w=384&q=100", "id":0},
               {"name": "Xiaomi TV A Pro 65", "price": 1700,
                "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2F3a8c41b4-ea85-4bd4-a982-e38120a7159f_Thumb.jpeg&w=384&q=100", "id":1},
               {"name": "Xiaomi TV Q2 65 Global Version", "price": 3000,
                "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2Fdf648fa0-7b4d-47b9-b149-ed4bc7d43551_Thumb.jpeg&w=384&q=100", "id":2},
               {"name": "Samsung TV UE43CU7172UXXH", "price": 1000,
                "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2Fa49e1947-775c-47d5-b094-1ffb2095b158_Thumb.jpeg&w=384&q=100", "id":3},
               {"name": "Samsung TV QE50Q60CAUXXH-2023-ტელევიზორი", "price": 2000,
                "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2F94fcdc28-aacf-42ed-8e73-0f5ae2dee362_Thumb.jpeg&w=384&q=100", "id":4},
               {"name": "Xiaomi TV A2 50 Global Version", "price": 1500,
                "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2F47c96af0-327e-4a9a-bb74-5bef8f435928_Thumb.jpeg&w=384&q=100", "id":5}]

leptops = [{
               "name": "Asus TUF 15 FA506NCR-HN044, AMD Ryzen 7-7435HS, Nvidia GeForce RTX 3050 4GB, 16GB RAM SSD 512GB, Free Dos, ლეპტოპი",
               "price": 3200,
               "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2F77dbeece-e1d5-4ab6-8e7d-1889024374e2_Thumb.jpeg&w=384&q=100", "id":0},
           {
               "name": "Apple MacBook Air 13 inch 2022 MLXW3LL/A M2 Chip 8GB/256GB SSD Space Grey, Apple M2(5nm), Apple 8-core GPU, 8GB RAM SSD 256GB, MacOS, ლეპტოპი",
               "price": 3500,
               "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fzoommer-images%2Fthumbs%2F0171989_apple-macbook-air-13-inch-2022-mlxw3lla-m2-chip-8gb256gb-ssd-space-grey-apple-m25nm-apple-8-core-gpu_550.jpeg&w=384&q=100", "id":1},
           {"name": "MSI Thin 15 9S7-16R831-2003 Black", "price": 3700,
            "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2F20acb0a5-07dd-4ad8-af26-829ed6779c8f_Thumb.jpeg&w=384&q=100", "id":2},
           {"name": "Lenovo Yoga 7 82YL005LRK Grey", "price": 1700,
            "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2F01d9e8b5-0fa2-4693-a47e-374657fbc4f8_Thumb.jpeg&w=384&q=100", "id":3},
           {
               "name": "Asus ROG Strix G16 G614JU-N3186, Intel Core i7-13650HX, Nvidia GeForce RTX 4050 6GB, 16GB RAM SSD 512GB, Free Dos, ლეპტოპი",
               "price": 4500,
               "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2F15d911b1-9ea8-4703-8c38-6e55746bf5b2_Thumb.jpeg&w=384&q=100", "id":4},
           {
               "name": "HP Pavilion Aero 13 A1WC9EA, AMD Ryzen 5-8640U, AMD Radeon Graphics, 16GB RAM SSD 512GB, Free Dos, ლეპტოპი",
               "price": 2500,
               "img": "https://zoommer.ge/_next/image?url=https%3A%2F%2Fs3.zoommer.ge%2Fsite%2Fa71fa01d-6cb0-4e07-ab1f-c048363f398d_Thumb.jpeg&w=384&q=100", "id":5}]




@app.route("/")
def home():
    products = Product.query.all()
    if current_user.is_authenticated:
        role = current_user.role
        admin = role=="admin"

    else:
        admin = False
        

    return render_template("Davaleba.html", products=products, admin=admin, User=User, )


@app.route("/Meore")
def second():
    products = Product.query.all()
    return render_template("Meore.html", ragacas=ragacas)


@app.route("/Register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user:
            username_taken = True
            print("Already Exsitin")

        if not user:
            print("succs")
            username_taken = False


            new_user = User(username=form.username.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        return render_template("Register.html", msg=username_taken, form=form)

    return render_template("Register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("You Passed Login")
            return redirect("/")


    return render_template("Sign.html", form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/support", methods=["GET", "POST"])
@login_required
def submit_contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_message = ContactMessage(username=form.username.data, email=form.email.data, message=form.message.data)
        db.session.add(new_message)
        db.session.commit()

        return redirect('/thank_you')

    return render_template("support.html", form=form)

@app.route('/thank_you')
def thank_you():
    return "Thank you For Your Message!"



@app.route("/Playstation")
def playstation():
    return render_template("playstation.html", playstations=playstations)


@app.route("/Television")
def television():
    return render_template("television.html", televisions=televisions)


@app.route("/Leptop")
def Laptop():
    return render_template("leptop.html", leptops=leptops)


@app.route("/create_product", methods=["GET", "POST"])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data)

        image = form.img.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)

        new_product.img = image.filename

        db.session.add(new_product)
        db.session.commit()

    return render_template("create_product.html", form=form)

@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data

        db.session.commit()
        return redirect("/")
    return render_template("create_product.html", form=form)



@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()

    return redirect("/")



@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get(product_id)
    return render_template("product_detail.html", product=product)

@app.route("/productss/<int:productss_id>")
def productss(productss_id):
    return render_template("product_detail2.html", productss=ragacas[productss_id])

@app.route("/produc/<int:produc_id>")
def produc(produc_id):
    return render_template("product_detail3.html", produc=playstations[produc_id])

@app.route("/product4/<int:product4_id>")
def product4(product4_id):
    return render_template("product_detail4.html", product4=televisions[product4_id])

@app.route("/product5/<int:product5_id>")
def product5(product5_id):
    return render_template("product_detail5.html", product5=leptops[product5_id])

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

