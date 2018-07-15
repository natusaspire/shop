from flask import (
    Blueprint,
    render_template,
    redirect
)

from sqlalchemy.sql import func

from app import db

from app.shop.models import (
    Country,
    Manufacturer,
    Category,
    Product,
    Client,
    Order
)

from app.shop.forms import (
    CountryForm,
    ManufacturerForm,
    CategoryForm,
    ProductForm,
    ClientForm,
    OrderForm
)


shop = Blueprint('shop', __name__, template_folder='templates')


@shop.route('/')
def get_index():
    return redirect('/stats')


@shop.route('countries')
def get_countries():
    countries = Country.query.all()

    return render_template('countries.html', countries=countries)


@shop.route('add-country', methods=['GET', 'POST'])
def add_country():
    form = CountryForm()

    if form.validate_on_submit():
        try:
            country = Country(name=form.name.data)

            db.session.add(country)
            db.session.commit()

            return redirect('/add-country')
        except:
            db.session.rollback()

    return render_template('add_country.html', form=form)


@shop.route('manufacturers')
def get_manufacturers():
    manufacturers = Manufacturer.query.all()

    return render_template('manufacturers.html', manufacturers=manufacturers)


@shop.route('add-manufacturer', methods=['GET', 'POST'])
def add_manufacturer():
    form = ManufacturerForm()

    if form.validate_on_submit():
        try:
            manufacturer = Manufacturer(
                name=form.name.data,
                website=form.website.data,
                country=form.country.data,
                amount_of_employees=form.amount_of_employees.data
            )

            db.session.add(manufacturer)
            db.session.commit()

            return redirect('/add-manufacturer')
        except:
            db.session.rollback()

    return render_template('add_manufacturer.html', form=form)


@shop.route('categories')
def get_categories():
    categories = Category.query.all()

    return render_template('categories.html', categories=categories)


@shop.route('add-category', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()

    if form.validate_on_submit():
        try:
            category = Category(name=form.name.data)

            db.session.add(category)
            db.session.commit()

            return redirect('/add-category')
        except:
            db.session.rollback()

    return render_template('add_category.html', form=form)


@shop.route('products')
def get_products():
    products = Product.query.order_by(Product.id.desc()).all()

    return render_template('products.html', products=products)


@shop.route('add-product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        try:
            product = Product(
                name=form.name.data,
                manufacturer=form.manufacturer.data,
                category=form.category.data,
                home_page=form.home_page.data,
                price=form.price.data
            )

            db.session.add(product)
            db.session.commit()

            return redirect('/add-product')
        except:
            db.session.rollback()

    return render_template('add_product.html', form=form)


@shop.route('clients')
def get_clients():
    clients = Client.query.all()

    return render_template('clients.html', clients=clients)


@shop.route('add-client', methods=['GET', 'POST'])
def add_client():
    form = ClientForm()

    if form.validate_on_submit():
        try:
            client = Client(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone_number=form.phone_number.data,
                email=form.email.data
            )

            db.session.add(client)
            db.session.commit()

            return redirect('/add-client')
        except:
            db.session.rollback()

    return render_template('add_client.html', form=form)


@shop.route('stock')
def get_stock():
    products = Product.query.filter(
        Product.in_stock==True
    ).order_by(
        Product.id.desc()
    ).all()

    return render_template('stock.html', products=products)


@shop.route('orders')
def get_orders():
    orders = Order.query.order_by(Order.date_and_time.desc()).all()

    return render_template('orders.html', orders=orders)


@shop.route('add-order', methods=['GET', 'POST'])
def add_order():
    form = OrderForm()

    if form.validate_on_submit():
        try:
            products = Product.query.filter(
                Product.id.in_([product.id for product in form.products.data])
            )

            order = Order(
                client=form.client.data,
                products=products.all(),
                total_price=products.with_entities(func.sum(Product.price))
            )

            db.session.add(order)

            db.session.query(Product).filter(
                Product.id.in_(products.with_entities(Product.id))
            ).update(
                dict(in_stock=False),
                synchronize_session='fetch'
            )

            db.session.commit()

            return redirect('/add-order')
        except:
            db.session.rollback()

    return render_template('add_order.html', form=form)


@shop.route('stats')
def get_stats():
    total_by_manufacturer = Product.get_total_price_by_every_manufacturer()

    total_by_category = Product.get_total_price_by_every_category()

    total_by_month = Order.get_total_price_by_every_month()

    return render_template(
        'stats.html',
        total_by_manufacturer=total_by_manufacturer,
        total_by_category=total_by_category,
        total_by_month=total_by_month
    )
