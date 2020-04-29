from service import db
from common.error import QueryFromSQLError, Insert2SQLError, DeleteFromSQLError


class Operator(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    backend = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    input = db.Column(db.String(80), nullable=False)
    output = db.Column(db.String(80), nullable=False)
    dimension = db.Column(db.Integer, nullable=False)
    metric_type = db.Column(db.String(120), nullable=False)
    endpoint = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<name %r>' % self.name


def search_operator(name=None):
    try:
        if name:
            res = db.session.query(Operator).filter(Operator.name == name).first()
        else:
            res = db.session.query(Operator, Operator.name).all()
        return res
    except Exception as e:
        raise QueryFromSQLError("query from sql error", e.orig.args[-1])


def insert_operator(operator):
    try:
        db.session.add(operator)
        db.session.commit()
    except Exception as e:
        raise Insert2SQLError("Insert operator to sql error", e.orig.args[-1])


def del_operator(name):
    try:
        res = db.session.query(Operator).filter(Operator.name == name).first()
        db.session.query(Operator).filter(Operator.name == name).delete()
        db.session.commit()
        return res
    except Exception as e:
        raise DeleteFromSQLError("delete from sql error", e.orig.args[-1])
