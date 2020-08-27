import os
import logging
import grpc
from concurrent import futures
import rpc.rpc_pb2
import rpc.rpc_pb2_grpc
from face_embedding import run, EmbedFaces as Encoder

ENDPOINT = os.getenv("OP_ENDPOINT", "127.0.0.1:80")


class OperatorServicer(rpc.rpc_pb2_grpc.OperatorServicer):
    def __init__(self):
        self.encoder = Encoder()

    def Execute(self, request, context):
        logging.info("execute")
        grpc_vectors = []
        vectors = run(self.encoder, request.datas, request.urls)
        for vector in vectors:
            v = rpc.rpc_pb2.Vector(element=vector)
            grpc_vectors.append(v)
        return rpc.rpc_pb2.ExecuteReply(nums=len(vectors),
                                        vectors=grpc_vectors,
                                        metadata=[])

    def Healthy(self, request, context):
        logging.info("healthy")
        return rpc.rpc_pb2.HealthyReply(healthy="healthy")

    def Identity(self, request, context):
        logging.info("identity")
        encoder = self.encoder
        return rpc.rpc_pb2.IdentityReply(name=encoder.name,
                                         endpoint=ENDPOINT,
                                         type=encoder.type,
                                         input=encoder.input,
                                         output=encoder.output,
                                         dimension=encoder.dimension,
                                         metricType=encoder.metric_type)


def serve(port):
    options = [('grpc.max_send_message_length', 100 * 1024 * 1024),
               ('grpc.max_receive_message_length', 100 * 1024 * 1024)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
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
