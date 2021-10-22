from web import app
from web.my_utils import PROD_FLAG

from flask import flash

if __name__ == '__main__':
    app.run(debug=True)