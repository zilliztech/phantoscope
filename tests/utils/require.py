from operators.operator import regist_operators, delete_operators


class PreResource:
    def create(self, data):
        pass

    def delete(self, data):
        pass

class PreOperator(PreResource):
    def create(self, data):
        regist_operators(data['endpoint'], data['name'])

    def delete(self, data):
        delete_operators(data['name'])
