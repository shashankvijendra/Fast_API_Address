"""
file : main.py
Description :  Fast APIS
Author : Shashank.V
"""

from fastapi import FastAPI, Depends
from typing import Optional, List
from sqlalchemy.orm import Session
from coordinates import location_address 
from database import *
import uvicorn

app = FastAPI()


@app.put('/place/{id}')
def update_places(id: int,request: Address, db: Session = Depends(get_db)):
    """
    Update the address based on ID
    """
    address_obj = db.query(DBPlace).filter(DBPlace.id == id)
    if not address_obj:
        return {"message": "Not Found"}
    location_address_val = location_address(request.coordinates)
    if not location_address_val:
        return {"message": "Error Try after some time"}
    address_obj.update(
        {
        'address':location_address_val, 
        'coordinates': request.coordinates,
        "is_true": request.is_true
        })
    db.commit()
    return {"message":"Update Success"}


@app.delete('/place/{id}')
def delete_place(id: int, db: Session = Depends(get_db)):
    """
    Delete the address based on ID
    """
    address_obj = db.query(DBPlace).filter(DBPlace.id == id)
    if not address_obj:
        return {"message": "Not Found"}
    address_obj.delete()
    db.commit()
    return {"message":"Delete Success"}


@app.post('/places/', response_model=Address)
def create_places_view(place: Address, db: Session = Depends(get_db)):
    """
        create the address
    """
    loc_address = location_address(place.coordinates)
    if not loc_address:
        return False
    place.address = loc_address
    db_place = create_place(db, place)
    if not db_place:
        return {'message': 'Failed'}
    return db_place


@app.get('/places/', response_model=List[Address])
def get_places_view(db: Session = Depends(get_db)):
    """
    Fetch All address available in db
    """
    return get_places(db)


@app.get('/place/{id}')
def get_place_view(id: int, db: Session = Depends(get_db)):
    """
    Fetch the address based on ID
    """
    return get_place(db, id)


@app.get('/place/{id}')
def get_filter_based_user(id: int, db: Session = Depends(get_db)):
    """
    Fetch the address based on ID
    """
    return get_place(db, id)


@app.get('/')
async def root():
    """
    Welcome URL
    """
    return {'message': 'Welcome'}    


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)
