# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
from service import db
from common.error import Insert2SQLError, QueryFromSQLError, DeleteFromSQLError, UpdateFromSQLError, NotExistError


class Pipeline(db.Model):
    name = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    description = db.Column(db.String(240), unique=False, nullable=True)
    processors = db.Column(db.String(240), unique=False, nullable=False)
    encoder = db.Column(db.String(240), unique=False, nullable=False)
    input = db.Column(db.String(120), unique=False, nullable=False)
    output = db.Column(db.String(120), unique=False, nullable=False)
    dimension = db.Column(db.Integer, unique=False, nullable=False)
    index_file_size = db.Column(db.Integer, unique=False, nullable=False)
    metric_type = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<Pipeline %r>' % self.name


def insert_pipeline(p):
    try:
        db.session.add(p)
        db.session.commit()
    except Exception as e:
        raise Insert2SQLError("insert to sql error", e.orig.args[-1])


def search_pipeline(name=None):
    try:
        if name:
            res = db.session.query(Pipeline).filter(Pipeline.name==name).first()
        else:
            res = db.session.query(Pipeline, Pipeline.name).all()
        return res
    except Exception as e:
        raise QueryFromSQLError("query from sql error", e.orig.args[-1])


def del_pipeline(name):
    try:
        res = db.session.query(Pipeline).filter(Pipeline.name==name).all()
        db.session.query(Pipeline).filter(Pipeline.name==name).delete()
        db.session.commit()
        return res
    except Exception as e:
        raise DeleteFromSQLError("delete from sql error", e.orig.args[-1])


def update_pipeline(name, p):
    try:
        old = db.session.query(Pipeline).filter(Pipeline.name==name).first()
        if not old:
            raise NotExistError("update target not exist", "pipeline with %s not exist" % name)
        for k, v in p.__dict__.items():
            if v and k != "_sa_instance_state":
                setattr(old, k, v)
        db.session.commit()
        return old
    except Exception as e:
        if isinstance(e, NotExistError):
            raise e
        raise UpdateFromSQLError("update from sql error", e.orig.args[-1])
