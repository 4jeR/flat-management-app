from web import db
from web.models import Flat

from web.models import Room

import json

db.drop_all()
db.create_all()

def load_json_data(print_=True):
    with open('web/flat_info.json', 'r') as f:
        flat_kwargs = json.loads(f.read())

    flat_objects = []
    for flat in flat_kwargs:
        d = dict((k, flat[k]) for k in flat.keys() if k not in ['rooms', 'location_photo'])
        flat_obj = Flat(**d)
        flat_objects.append(flat_obj)

    if print_:
        for f in flat_objects:
            print(f.__dict__)


if __name__ == '__main__':
    load_json_data(False)
    # id = db.Column(db.Integer, primary_key=True)
    # composed_name = db.Column(db.String, unique=False, nullable=False)
    # full_address = db.Column(db.String, unique=True, nullable=False)
    # city = db.Column(db.String, unique=False, nullable=False)
    # rooms_count = db.Column(db.Integer, unique=False, nullable=False)
    # block_number = db.Column(db.Integer, unique=False, nullable=False)
    # flat_number = db.Column(db.Integer, unique=False, nullable=False)
    # postal_code = db.Column(db.String, unique=False, nullable=False)
    # block_entry_code = db.Column(db.String, unique=False, nullable=False)
    # total_area = db.Column(db.Integer, unique=False, nullable=False)


