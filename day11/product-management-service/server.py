from product import product, db
from product.api.product_api import ProductApi


if __name__ == '__main__':
    db.create_all()
    product.run()