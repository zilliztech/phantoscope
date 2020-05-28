from service import db
from common.error import Insert2SQLError, QueryFromSQLError, DeleteFromSQLError


class Mapping(db.Model):
    id = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    app_name = db.Column(db.String(120), db.ForeignKey('application.name'), nullable=False)
    app = db.relationship('Application', foreign_keys=app_name)
    image_url = db.Column(db.String(500), nullable=True)
    fields = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return '<Mapping %r>' % self.id


def add_mapping_data(mapping):
    try:
        db.session.add(mapping)
        db.session.commit()
    except Exception as e:
        raise Insert2SQLError("insert mapping to sql error", e.orig.args[-1])

def search_from_mapping(id):
    try:
        res = db.session.query(Mapping).filter(Mapping.id==id).first()
        return res
    except Exception as e:
        raise QueryFromSQLError("query from sql error", e.orig.args[-1])

def search_ids_from_mapping(ids):
    try:
        ids = [str(x) for x in ids]
        res = db.session.query(Mapping).filter(Mapping.id.in_(ids)).all()
        c = sorted(res, key = lambda x: ids.index(x.id))
        return res
    except Exception as e:
        raise QueryFromSQLError("query from sql error", e.orig.args[-1])


def search_by_application(app, limit, offset):
    try:
        res = db.session.query(Mapping).filter(Mapping.app_name==app).limit(limit).offset(offset).all()
        return res
    except Exception as e:
        raise QueryFromSQLError("query from sql error", e.orig.args[-1])


def del_mapping(id):
    try:
        res = db.session.query(Mapping).filter(Mapping.id==id).all()
        db.session.query(Mapping).filter(Mapping.id==id).delete()
        db.session.commit()
        return res
    except Exception as e:
        raise DeleteFromSQLError("delete from sql error", e.orig.args[-1])
