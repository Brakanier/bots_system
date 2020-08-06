from tortoise.models import Model
from tortoise import fields

class Sub(Model):
    id = fields.IntField(pk=True)
    account = fields.ForeignKeyField('models.Account', 'subs')
    channel_name = fields.CharField(max_length=32)
    created = fields.DatetimeField(auto_now_add=True)
    unsub_datetime = fields.DatetimeField()
    
