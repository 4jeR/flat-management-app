import json
from web.models import Flat
import os
from copy import deepcopy
import datetime


PROD_FLAG = False

PATH =  '/home/4jeR/krk-flats/web' if PROD_FLAG else 'web' 


def load_flat_json_data():
    with open(f'{PATH}/flat_info.json', 'r') as f:
        flat_kwargs = json.loads(f.read())

    flat_objects = []
    for flat in flat_kwargs:
        d = dict((k, flat[k]) for k in flat.keys())
        flat_obj = Flat(**d)
        flat_objects.append(flat_obj)

    return flat_objects

def load_contract_json_data():
    with open(f'{PATH}/contracts.json', 'r') as f:
        contract_kwargs = json.loads(f.read())
        return contract_kwargs

def get_flat_from_id(flat_id):
    flats = load_flat_json_data()
    for flat in flats:
        if flat.id == flat_id:
            return flat
    return None

def get_contract_from_id(contract_id):
    contracts = load_contract_json_data()
    for contract in contracts:
        if contract['idx'] == contract_id:
            return contract
    return None 


def get_common_photos(flat):
    photos = [f'{flat.photos_path}/common/{photo}' for photo in os.listdir(f'{PATH}/static/{flat.photos_path}/common/') if photo.endswith('.jpg')]
    return photos

def get_room_photos(flat, idx):
    photos = [f'{flat.photos_path}/room_{idx}/{photo}' for photo in os.listdir(f'{PATH}/static/{flat.photos_path}/room_{idx}/') if photo.endswith('.jpg')]
    return photos

def get_rooms_occupied(flats):
    kwargs = {
        'total_rooms': 0,
        'occupied_rooms': 0
    }
    for flat in flats:
        kwargs['total_rooms'] += int(flat.rooms_count)
        for room in flat.rooms:
            kwargs['occupied_rooms'] += room.occupied
    
    return kwargs

def _find_index(l, key_index, key_roomid):
    for i, contract in enumerate(l):
        if str(contract['idx']) == str(key_index) and str(contract['room_id']) == str(key_roomid):
            return i
    return None

def _update_flat_info(flats_content, flat_id, room_id, idx, remove_contract=False):
    '''
    This is callback after contract update. 
    should be probably moved as decorator to assure corectness
    '''
    for flat in flats_content:
        if flat['id'] == str(flat_id):
            for room in flat['rooms']:
                if room['idx'] == str(room_id):
                    room['contract_id'] = '-1' if remove_contract else str(idx)
                    room['occupied'] = not remove_contract


def date_to_args(date_str):
    x = date_str[:10].split('-')
    x.reverse()
    x = map(lambda v: int(v), x)
    print(f"TUPLE: {x}")
    return tuple(x)

def calc_progress_bar(contract):
    start = contract['start_date']
    end = contract['end_date']
    date_start = datetime.date(*date_to_args(start))
    date_end = datetime.date(*date_to_args(end))
    date_today = datetime.date.today()

    X = (date_today - date_start).days
    print(X)
    A = 0
    B = (date_end - date_start).days
    print(B)
    C = 0
    D = 100
    value = (X-A)/(B-A) * (D-C) + C

    print(f"VALUE ->>>>>>>>>> {value}")

    '''
if your number X falls between A and B, and you would like Y to fall between C and D, you can apply the following linear transform:

Y = (X-A)/(B-A) * (D-C) + C
'''


    # need to value between 1-100
    return f'width: {value}%'


def date_to_string(date_str):
    print(date_str)
    s2 = date_str[:10].split('-')
    s2.reverse()
    s2 = '-'.join(s2)
    return s2

def add_contract(flat_id, idx, room_id, rent_price, first_name, last_name, phone_number, start_date, end_date):
    contract = {
        "idx": idx,
        "room_id": room_id,
        "rent_price": rent_price,
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "start_date": date_to_string(start_date),
        "end_date": date_to_string(end_date)
    }
    with open(f'{PATH}/contracts.json', 'r') as fp:
        contracts_content = fp.read()

    with open(f'{PATH}/flat_info.json', 'r') as fp:
        flats_content = fp.read()


    # get contents and save the backups...
    contract_content = json.loads(contracts_content)
    backup_contract_content = deepcopy(contract_content)

    flats_content = json.loads(flats_content)
    backup_flats_content = deepcopy(flats_content)

    
    _update_flat_info(flats_content, flat_id, room_id, idx)

    contract_content.append(contract)

    try:
        with open(f'{PATH}/contracts.json', 'w') as fp:
            json.dump(contract_content, fp=fp, indent=4, ensure_ascii=False)

        with open(f'{PATH}/flat_info.json', 'w') as fp:
            json.dump(flats_content, fp=fp, indent=4, ensure_ascii=False)
    except Exception:
        print(f"[FAIL][add_contract] couldn't add contract for flat id: {flat_id}, room id: {room_id}.")
        with open(f'{PATH}/contracts.json', 'w') as fp:
            json.dump(backup_contract_content, fp=fp, indent=4, ensure_ascii=False)

        with open(f'{PATH}/flat_info.json', 'w') as fp:
            json.dump(backup_flats_content, fp=fp, indent=4, ensure_ascii=False)


def remove_contract(flat_id, idx, room_id):
    with open(f'{PATH}/contracts.json', 'r') as fp:
        contracts_content = fp.read()

    with open(f'{PATH}/flat_info.json', 'r') as fp:
        flats_content = fp.read()


    # get contents and save the backups...
    contract_content = json.loads(contracts_content)
    backup_contract_content = deepcopy(contract_content)

    flats_content = json.loads(flats_content)
    backup_flats_content = deepcopy(flats_content)

    
    _update_flat_info(flats_content, flat_id, room_id, idx, remove_contract=True)

    contract_index = _find_index(contract_content, idx, room_id)
    if contract_index is not None:
        contract_content.pop(contract_index)


    try:
        with open(f'{PATH}/contracts.json', 'w') as fp:
            json.dump(contract_content, fp=fp, indent=4, ensure_ascii=False)

        with open(f'{PATH}/flat_info.json', 'w') as fp:
            json.dump(flats_content, fp=fp, indent=4, ensure_ascii=False)
    except Exception:
        print(f"[FAIL][add_contract] couldn't add contract for flat id: {flat_id}, room id: {room_id}.")
        with open(f'{PATH}/contracts.json', 'w') as fp:
            json.dump(backup_contract_content, fp=fp, indent=4, ensure_ascii=False)

        with open(f'{PATH}/flat_info.json', 'w') as fp:
            json.dump(backup_flats_content, fp=fp, indent=4, ensure_ascii=False)

