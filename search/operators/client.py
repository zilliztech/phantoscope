import grpc
import operators.rpc_pb2 as pb
import operators.rpc_pb2_grpc as rpc_pb2_grpc


def identity(endpoint):
    with grpc.insecure_channel(endpoint) as channel:
        stub = rpc_pb2_grpc.OperatorStub(channel)
        res = stub.Identity(pb.IdentityRequest())
        return {
            "name": res.name,
            "endpoint": res.endpoint,
            "type": res.type,
            "input": res.input,
            "output": res.output,
            "dimension": res.dimension,
            "metric_type": res.metricType
        }


def health(operator):
    try:
        with grpc.insecure_channel(operator.endpoint) as channel:
            stub = rpc_pb2_grpc.OperatorStub(channel)
            res = stub.Healthy(pb.HealthyRequest())
            return res.healthy
    except Exception as e:
        raise e


def execute(operator, datas=[], urls=[]):
    try:
        with grpc.insecure_channel(operator.endpoint) as channel:
            stub = rpc_pb2_grpc.OperatorStub(channel)
            res = stub.Execute(pb.ExecuteRequest(urls=urls, datas=datas))
            return [list(x.element) for x in res.vectors], res.metadata
    except Exception as e:
        raise e
