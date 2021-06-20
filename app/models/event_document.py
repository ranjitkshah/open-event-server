from app.models import db
from app.models.helpers.timestamp import Timestamp


class EventDocument(db.Model, Timestamp):
    __tablename__ = 'event_documents'
    __table_args__ = (db.UniqueConstraint('name', 'event_id', name='uq_ed_name_event'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    document_url = db.Column(db.String, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'))

    event = db.relationship("Event", backref='event_documents')
