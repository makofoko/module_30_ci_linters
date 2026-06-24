from module_29_testing.hw.models import Client, Parking
import pytest
from factories import ClientFactory, ParkingFactory

def test_create_client_factory(_db):
    client = ClientFactory()
    _db.session.add(client)
    _db.session.commit()
    assert client.id is not None

def test_create_parking_factory(_db):
    parking = ParkingFactory()
    _db.session.add(parking)
    _db.session.commit()
    assert parking.id is not None