from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Receptionist(db.Model):
    __tablename__ = 'receptionists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    checklists = db.relationship('Checklist', backref='receptionist', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'active': self.active
        }


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    building = db.Column(db.String(20), nullable=False)
    checklists = db.relationship('Checklist', backref='room', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'building': self.building
        }


class Checklist(db.Model):
    __tablename__ = 'checklists'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    receptionist_id = db.Column(db.Integer, db.ForeignKey('receptionists.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Estado de la habitación (disponible / ocupada)
    estado = db.Column(db.String(15), nullable=False, default='')
    # Luz central (ok, x)
    luz_central = db.Column(db.String(5), nullable=False, default='')
    # Sensor (ok, x)
    sensor = db.Column(db.String(5), nullable=False, default='')
    # Cobertores (ok, x)
    cobertores = db.Column(db.String(5), nullable=False, default='')
    # Cambio de sábanas (ok, x)
    cambio_sabanas = db.Column(db.String(5), nullable=False, default='')
    # Velador (ok, x)
    velador = db.Column(db.String(5), nullable=False, default='')
    # Almohada (ok, x)
    almohada = db.Column(db.String(5), nullable=False, default='')
    # Extractor (ok, x)
    extractor = db.Column(db.String(5), nullable=False, default='')
    # Estufa (ok, x)
    estufa = db.Column(db.String(5), nullable=False, default='')
    # Basurero (ok, x)
    basurero = db.Column(db.String(5), nullable=False, default='')
    # Humidificador (ok, x)
    humidificador = db.Column(db.String(5), nullable=False, default='')
    # Cortina (ok, x)
    cortina = db.Column(db.String(5), nullable=False, default='')
    # Blackout (ok, x)
    blackout = db.Column(db.String(5), nullable=False, default='')
    # Aseo general (ok, x)
    aseo_general = db.Column(db.String(5), nullable=False, default='')
    # Closet (ok, x)
    closet = db.Column(db.String(5), nullable=False, default='')
    # Observaciones
    observaciones = db.Column(db.Text, default='')

    OKX_FIELDS = [
        'luz_central', 'sensor', 'cobertores', 'cambio_sabanas',
        'velador', 'almohada', 'extractor', 'estufa', 'basurero',
        'humidificador', 'cortina', 'blackout', 'aseo_general', 'closet'
    ]

    def to_dict(self):
        return {
            'id': self.id,
            'room_code': self.room.code,
            'room_building': self.room.building,
            'receptionist_name': self.receptionist.name,
            'receptionist_id': self.receptionist_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'date_only': self.created_at.strftime('%Y-%m-%d'),
            'estado': self.estado,
            'luz_central': self.luz_central,
            'sensor': self.sensor,
            'cobertores': self.cobertores,
            'cambio_sabanas': self.cambio_sabanas,
            'velador': self.velador,
            'almohada': self.almohada,
            'extractor': self.extractor,
            'estufa': self.estufa,
            'basurero': self.basurero,
            'humidificador': self.humidificador,
            'cortina': self.cortina,
            'blackout': self.blackout,
            'aseo_general': self.aseo_general,
            'closet': self.closet,
            'observaciones': self.observaciones
        }

    @property
    def ok_count(self):
        return sum(1 for f in self.OKX_FIELDS if getattr(self, f) == 'ok')

    @property
    def issue_count(self):
        return sum(1 for f in self.OKX_FIELDS if getattr(self, f) == 'x')
