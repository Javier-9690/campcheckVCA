"""Seed the VCA database tables. Run on deployment."""
from app import app
from models import db, Room, Checklist
from rooms_data import get_all_rooms


def seed():
    with app.app_context():
        # Crea las tablas vca_rooms, vca_checklists, vca_receptionists
        # sin tocar las tablas del sistema anterior (rooms, checklists, receptionists)
        db.create_all()
        print("Tablas VCA verificadas.")

        # Insertar habitaciones solo si la tabla está vacía
        if Room.query.first() is None:
            vca_rooms = get_all_rooms()
            for code, building in vca_rooms:
                db.session.add(Room(code=code, building=building))
            db.session.commit()
            n_modules = len(set(b for _, b in vca_rooms))
            print(f"Insertadas {len(vca_rooms)} habitaciones VCA en {n_modules} módulos.")
        else:
            print(f"Habitaciones VCA ya presentes ({Room.query.count()}). Sin cambios.")

        print("Listo.")


if __name__ == '__main__':
    seed()
