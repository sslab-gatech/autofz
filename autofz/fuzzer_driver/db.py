import peewee

db_proxy = peewee.DatabaseProxy()


class BaseModel(peewee.Model):
    class Meta:
        database = db_proxy


class AFLModel(BaseModel):
    seed = peewee.CharField()
    output = peewee.CharField()
    group = peewee.CharField()
    program = peewee.CharField()
    argument = peewee.CharField()
    master = peewee.BooleanField()
    pid = peewee.IntegerField()
    fuzzer_id = peewee.IntegerField(unique=True)


class QSYMModel(BaseModel):
    seed = peewee.CharField()
    output = peewee.CharField()
    group = peewee.CharField()
    program = peewee.CharField()
    argument = peewee.CharField()
    afl_name = peewee.CharField()
    pid = peewee.IntegerField()


class AngoraModel(BaseModel):
    seed = peewee.CharField()
    output = peewee.CharField()
    group = peewee.CharField()
    program = peewee.CharField()
    argument = peewee.CharField()
    thread = peewee.IntegerField()
    pid = peewee.IntegerField()


class LibFuzzerModel(BaseModel):
    seed = peewee.CharField()
    output = peewee.CharField()
    group = peewee.CharField()
    program = peewee.CharField()
    argument = peewee.CharField()
    thread = peewee.IntegerField()
    pid = peewee.IntegerField()


class ControllerModel(BaseModel):
    scale_num = peewee.IntegerField()


DB = {}
