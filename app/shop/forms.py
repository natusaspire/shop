from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    IntegerField
)

from wtforms.fields.html5 import (
    EmailField,
    URLField
)

from wtforms.validators import (
    InputRequired,
    Email,
    URL,
    Optional,
    NumberRange
)

from wtforms_sqlalchemy.fields import (
    QuerySelectField,
    QuerySelectMultipleField
)

from app.shop.models import (
    Country,
    Manufacturer,
    Category,
    Product,
    Client,
    Order
)


class CountryForm(FlaskForm):
    name = StringField(validators=[InputRequired()])


class ManufacturerForm(FlaskForm):
    name = StringField(validators=[InputRequired()])
    website = StringField()

    country = QuerySelectField(
        query_factory=lambda: Country.query,
        get_pk=lambda country: country.id,
        validators=[InputRequired()]
    )

    amount_of_employees = IntegerField(
        validators=[Optional(), NumberRange(min=0)]
    )


class CategoryForm(FlaskForm):
    name = StringField(validators=[InputRequired()])


class ProductForm(FlaskForm):
    name = StringField(validators=[InputRequired()])

    manufacturer = QuerySelectField(
        query_factory=lambda: Manufacturer.query,
        get_pk=lambda manufacturer: manufacturer.id,
        validators=[InputRequired()]
    )

    category = QuerySelectField(
        query_factory=lambda: Category.query,
        get_pk=lambda category: category.id,
        validators=[InputRequired()]
    )

    home_page = URLField(validators=[URL(), Optional()])
    price = IntegerField(validators=[InputRequired(), NumberRange(min=1)])


class ClientForm(FlaskForm):
    first_name = StringField(validators=[InputRequired()])
    last_name = StringField(validators=[InputRequired()])
    phone_number = StringField(validators=[InputRequired()])
    email = EmailField(validators=[InputRequired(), Email()])


class OrderForm(FlaskForm):
    client = QuerySelectField(
        query_factory=lambda: Client.query,
        get_pk=lambda client: client.id,
        validators=[InputRequired()]
    )

    products = QuerySelectMultipleField(
        query_factory=lambda: Product.query.filter(Product.in_stock==True),
        get_pk=lambda product: product.id,
        validators=[InputRequired()]
    )
