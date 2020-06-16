import os
import logging
import grpc
from concurrent import futures
import rpc.rpc_pb2
import rpc.rpc_pb2_grpc
from custom_operator import CustomOperator as Operator

ENDPOINT = os.getenv("OP_ENDPOINT", "127.0.0.1:80")


class OperatorServicer(rpc.rpc_pb2_grpc.OperatorServicer):
    def __init__(self):
        self.operator = Operator()

    def Execute(self, request, context):
        logging.info("execute")
        # encoder code which returns vectors
        grpc_vectors = []
        vectors = self.operator.run(request.datas, request.urls)
        for vector in vectors:
            v = rpc.rpc_pb2.Vector(element=vector)
            grpc_vectors.append(v)
        return rpc.rpc_pb2.ExecuteReply(nums=len(vectors),
                                        vectors=grpc_vectors,
                                        metadata=[])
        # # processor code which returns base64 images
        # grpc_metas = []
        # result_images = run(self.operator, request.datas, request.urls)
        # result_images = result_images[0]
        # for result_image in result_images:
        #     data = rpc.rpc_pb2.MetaData(data=bytes(result_image, encoding='utf-8'))
        #     grpc_metas.append(data)
        # return rpc.rpc_pb2.ExecuteReply(nums=len(grpc_metas),
        #                                 vectors=[],
        #                                 metadata=grpc_metas)

    def Healthy(self, request, context):
        logging.info("healthy")
        return rpc.rpc_pb2.HealthyReply(healthy="healthy")

    def Identity(self, request, context):
        logging.info("identity")
        operator = self.operator
        return rpc.rpc_pb2.IdentityReply(name=operator.name,
                                         endpoint=ENDPOINT,
                                         type=operator.type,
                                         input=operator.input,
                                         output=operator.output,
                                         dimension=operator.dimension,
                                         metricType=operator.metric_type)


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.rpc_pb2_grpc.add_OperatorServicer_to_server(OperatorServicer(), server)
    server.add_insecure_port('[::]:%s' % port)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter)
    port = ENDPOINT.split(":")[-1]
    logging.info("Start server")
    serve(port)
