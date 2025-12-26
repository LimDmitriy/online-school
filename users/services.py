from config.settings import STRIPE_API_KEY
import stripe
from forex_python.converter import CurrencyRates, RatesNotAvailableError


stripe.api_key = STRIPE_API_KEY
DEFAULT_RATE = 0.011


def convert_rub_to_dollars(amount):
    """Конвертация рубля в доллары"""

    return int(amount * DEFAULT_RATE)


def create_stripe_price(amount):
    """Создает цену в stripe"""
    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "Payment"},
    )


def create_stripe_session(price):
    """Создает сессию для оплаты в stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
