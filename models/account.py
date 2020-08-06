from tortoise.models import Model
from tortoise import fields

class Account(Model):
    id = fields.IntField(pk=True)
    login = fields.CharField(max_length=32)
    
    created = fields.DatetimeField(auto_now_add=True)
