from peewee import *
import datetime

db = SqliteDatabase('tasks.sqlite')
class BaseModel(Model):
    class Meta:
        database = db

class Task(BaseModel):
    title = CharField(unique=True)
    description = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

db.connect()
db.create_tables([Task])