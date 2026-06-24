from flask import Blueprint, request, jsonify
from .extensions import db
from .models import Client, Parking, ClientParking
from datetime import datetime

bp = Blueprint("main", __name__)

@bp.route("/clients")
def get_clients():
    clients = Client.query.all()
    return jsonify([{"id": c.id, "name": c.name, "surname": c.surname} for c in clients])

@bp.route("/clients/<int:client_id>")
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify({"id": client.id, "name": client.name, "surname": client.surname})

@bp.route("/clients", methods=["POST"])
def create_client():
    data = request.json
    client = Client(**data)
    db.session.add(client)
    db.session.commit()
    return jsonify({"id": client.id}), 201

@bp.route("/parkings", methods=["POST"])
def create_parking():
    data = request.json
    parking = Parking(**data)
    db.session.add(parking)
    db.session.commit()
    return jsonify({"id": parking.id}), 201

@bp.route("/client_parkings", methods=["POST"])
def enter_parking():
    data = request.json
    parking = db.session.get(Parking, data["parking_id"])
    if not parking.opened or parking.count_available_places <= 0:
        return jsonify({"error": "Parking closed or full"}), 400
    client = db.session.get(Client, data["client_id"])
    if not client.credit_card:
        return jsonify({"error": "No credit card"}), 400
    log = ClientParking(client_id=client.id, parking_id=parking.id, time_in=datetime.now())
    parking.count_available_places -= 1
    db.session.add(log)
    db.session.commit()
    return jsonify({"message": "Car entered"}), 201

@bp.route("/client_parkings", methods=["DELETE"])
def exit_parking():
    data = request.json
    log = ClientParking.query.filter_by(client_id=data["client_id"], parking_id=data["parking_id"]).first_or_404()
    log.time_out = datetime.now()
    parking = db.session.get(Parking, log.parking_id)
    parking.count_available_places += 1
    db.session.commit()
    return jsonify({"message": "Car exited"}), 200

@bp.route("/parkings")
def get_parkings():
    parkings = Parking.query.all()
    return jsonify([{"id": p.id, "address": p.address, "opened": p.opened} for p in parkings])