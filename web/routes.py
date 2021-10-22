from web import app


from flask import render_template
from flask import redirect


from .my_utils import *
from flask import request
from flask import flash
from flask import url_for


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/overview', methods=['GET', 'POST'])
def v_overview():
    flats = load_flat_json_data()

    kwargs = get_rooms_occupied(flats)

    return render_template('overview.html', flats=flats, **kwargs)  




@app.route('/overview/<string:flat_id>', methods=['GET', 'POST'])
def v_flat(flat_id):
    flat = get_flat_from_id(flat_id)
    flat_images = get_common_photos(flat)

    for room in flat.rooms:
        room.add_photos(get_room_photos(flat, room.idx))

    return render_template('flat.html', flat=flat, images=flat_images)

@app.route('/contract/<string:flat_id>/<string:contract_id>', methods=['GET', 'POST'])
def v_contract(flat_id, contract_id):
    contract = get_contract_from_id(contract_id)
    progress_bar_value = calc_progress_bar(contract)
    '''todo:
    poprawic wyglad umowy + dodac telefon do kontraktu + download PDF?
    '''
    return render_template('contract.html', flat_id=flat_id, contract=contract, progress_bar_value=progress_bar_value)

@app.route('/new-contract/<string:flat_id>/<string:room_id>', methods=['GET', 'POST'])
def v_new_contract(flat_id, room_id):    
    if request.method == "POST":
        if request.form["submit"] == "submit_contract":
            contract = {
                "idx": f'{flat_id}{room_id}',
                "room_id": room_id,
                "rent_price": request.form['rent_price'],
                "first_name": request.form['first_name'],
                "last_name": request.form['last_name'],
                "phone_number": request.form['phone_number'],
                "start_date": request.form['start_date'],
                "end_date": request.form['end_date']
            }
            add_contract(flat_id, **contract)

            flash("Dodano umowę pomyślnie.", 'success')
            return redirect(url_for('v_flat', flat_id=flat_id))
        else:
            flash(f"Coś źle...", 'danger')

            return redirect(url_for('v_new_contract', flat_id=flat_id))
    return render_template('new_contract.html', flat_id=flat_id, room_id=room_id)

@app.route('/delete-contract/<string:flat_id>/<string:room_id>/<string:contract_id>', methods=['GET', 'POST'])
def v_delete_contract(flat_id, room_id, contract_id):    
    remove_contract(flat_id, contract_id, room_id)
    flash(f"Usunięto umowę.", 'success')
    return redirect(url_for('v_flat', flat_id=flat_id))


