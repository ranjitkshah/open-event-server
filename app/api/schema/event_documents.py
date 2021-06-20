from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from app.api.helpers.utilities import dasherize


class EventDocumentSchema(Schema):
    class Meta:
        type_ = 'event-document'
        self_view = 'v1.event_document_detail'
        self_view_kwargs = {'id': '<id>'}
        inflect = dasherize

    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    document_url = fields.Url(required=True)

    event = Relationship(
        self_view='v1.event_document_event',
        self_view_kwargs={'id': '<id>'},
        related_view='v1.event_detail',
        related_view_kwargs={'event_document_id': '<id>'},
        schema='EventSchema',
        type_='event',
    )
