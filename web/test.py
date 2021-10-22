import json
from copy import deepcopy



def _update_flat_info(flats_content, flat_id, room_id, idx):
    '''
    This is callback after contract update. 
    should be probably moved as decorator to assure corectness
    '''
    for flat in flats_content:
        print(f"""flat["id"] = {flat['id']} != {flat_id}""")
        if flat['id'] == str(flat_id):
            for room in flat['rooms']:
                print(f"""room["idx"] = {room['idx']} != {room_id}""")
                if room['idx'] == str(room_id):
                    room['contract_id'] = str(idx)
                    room['occupied'] = True

def add_contract(idx, flat_id, room_id, first_name, last_name, start_date, end_date):
    contract = {
        "idx": idx,
        "room_id": room_id,
        "first_name": first_name,
        "last_name": last_name,
        "start_date": start_date,
        "end_date": end_date
    }
    with open('contracts.json', 'r') as fp:
        contracts_content = fp.read()

    with open('flat_info.json', 'r') as fp:
        flats_content = fp.read()


    # get contents and save the backups...
    contract_content = json.loads(contracts_content)
    backup_contract_content = deepcopy(contract_content)

    flats_content = json.loads(flats_content)
    backup_flats_content = deepcopy(flats_content)

    
    _update_flat_info(flats_content, flat_id, room_id, idx)

    contract_content.append(contract)

    try:
        with open('contracts.json', 'w') as fp:
            json.dump(contract_content, fp=fp, indent=4, ensure_ascii=False)

        with open('flat_info.json', 'w') as fp:
            json.dump(flats_content, fp=fp, indent=4, ensure_ascii=False)
    except Exception:
        print(f"[FAIL][add_contract] couldn't add contract for flat id: {flat_id}, room id: {room_id}.")
        with open('contracts.json', 'w') as fp:
            json.dump(backup_contract_content, fp=fp, indent=4, ensure_ascii=False)

        with open('flat_info.json', 'w') as fp:
            json.dump(backup_flats_content, fp=fp, indent=4, ensure_ascii=False)

add_contract(69, 1, 2, 'bartek', 'dlugosz', '2021', '2033')

