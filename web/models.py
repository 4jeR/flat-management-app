

class Room:
    def __init__(self, idx, price, occupied, area, photos_path, flat_id, contract_id="-1"):
        self.idx = idx
        self.price = price
        self.occupied = occupied
        self.area = area
        self.photos_path = photos_path
        self.flat_id = flat_id
        self.contract = None
        self.photos = []
        self.contract_id = contract_id

    def add_contract(self, contract):
        self.contract = contract
        self.occupied = True
        

    def delete_contract(self):
        self.contract = None
        self.occupied = False
    
    def add_photos(self, photos):
        for photo in photos:
            self.photos.append(photo)

class Flat:
    def __init__(self, 
                id, 
                city, 
                short_name, 
                full_address,
                rooms,
                rooms_count,
                block_number,
                flat_number,
                postal_code,
                block_entry_code,
                total_area,
                location_photo,
                photos_path):
        self.id = id
        self.city = city
        self.short_name = short_name
        self.full_address = full_address
        self.rooms = [Room(**room) for room in rooms]
        self.rooms_count = rooms_count
        self.block_number = block_number 
        self.flat_number = flat_number 
        self.postal_code = postal_code 
        self.block_entry_code = block_entry_code 
        self.total_area = total_area 
        self.location_photo = location_photo
        self.photos_path = photos_path
        
    
class Contract:
    def __init__(self, idx, start_date, end_date, rent_price, pdf, **people):
        self.idx = idx
        self.start_date = start_date
        self.end_date = end_date
        self.rent_price = rent_price
        self.people = people

class Person:
    def __init__(self, first_name, last_name, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
