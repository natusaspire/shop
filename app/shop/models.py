from app import db

from sqlalchemy.sql import func


class Country(db.Model):
    __tablename__ = 'shop_country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __str__(self):
        return self.name


class Manufacturer(db.Model):
    __tablename__ = 'shop_manufacturer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    website = db.Column(db.String(255))

    country_id = db.Column(
        db.Integer,
        db.ForeignKey(Country.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False
    )

    amount_of_employees = db.Column(db.Integer)

    country = db.relationship(
        'Country',
        foreign_keys='Manufacturer.country_id'
    )

    def __str__(self):
        return self.name


class Category(db.Model):
    __tablename__ = 'shop_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    __tablename__ = 'shop_product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    manufacturer_id = db.Column(
        db.Integer,
        db.ForeignKey(Manufacturer.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey(Category.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False
    )

    home_page = db.Column(db.String(255))
    price = db.Column(db.Integer, nullable=False)
    in_stock = db.Column(db.Boolean, nullable=False, default=True)

    manufacturer = db.relationship(
        'Manufacturer',
        foreign_keys='Product.manufacturer_id'
    )

    category = db.relationship(
        'Category',
        foreign_keys='Product.category_id'
    )

    def __str__(self):
        return '%s (US$%s)' % (self.name, self.price / 100)

    @classmethod
    def get_total_price_by_every_manufacturer(cls):
        return cls.query.filter(
            cls.in_stock==False
        ).join(
            Manufacturer,
            cls.manufacturer_id==Manufacturer.id
        ).group_by(
            Manufacturer.id
        ).with_entities(
            Manufacturer.name,
            func.sum(cls.price)
        ).order_by(
            func.sum(cls.price).desc()
        ).all()

    @classmethod
    def get_total_price_by_every_category(cls):
        return cls.query.filter(
            cls.in_stock==False
        ).join(
            Category,
            cls.category_id==Category.id
        ).group_by(
            Category.id
        ).with_entities(
            Category.name,
            func.sum(cls.price)
        ).order_by(
            func.sum(cls.price).desc()
        ).all()


class Client(db.Model):
    __tablename__ = 'shop_client'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)

    orders = db.relationship('Order', backref='client')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


order_product = db.Table(
    'shop_order_product',

    db.Column(
        'id',
        db.Integer,
        primary_key=True
    ),

    db.Column(
        'order_id',
        db.Integer,
        db.ForeignKey('shop_order.id', onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False
    ),

    db.Column(
        'product_id',
        db.Integer,
        db.ForeignKey('shop_product.id', onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False
    )
)


class Order(db.Model):
    __tablename__ = 'shop_order'

    id = db.Column(db.Integer, primary_key=True)
    date_and_time = db.Column(db.DateTime, default=db.func.now())

    client_id = db.Column(
        db.Integer,
        db.ForeignKey(Client.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False
    )

    total_price = db.Column(db.Integer, nullable=False)

    products = db.relationship('Product', secondary=order_product)

    @classmethod
    def get_total_price_by_every_month(cls):
        return cls.query.group_by(
            func.strftime('%Y-%m', cls.date_and_time)
        ).order_by(
            func.strftime('%Y-%m', cls.date_and_time).desc()
        ).with_entities(
            func.strftime('%Y-%m', cls.date_and_time),
            func.sum(cls.total_price)
        ).all()
