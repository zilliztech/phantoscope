import os
import logging
import grpc
from concurrent import futures
import tensorflow as tf
from tensorflow import keras
import vggrpc.rpc_pb2
import vggrpc.rpc_pb2_grpc
from encoder import Vgg, run

ENDPOINT = os.getenv("OP_ENDPOINT", "127.0.0.1:50003")


def keras_config():
    config = tf.ConfigProto(
        device_count={'GPU': 1},
        intra_op_parallelism_threads=1,
        allow_soft_placement=True
    )

    config.gpu_options.allow_growth = True
    config.gpu_options.per_process_gpu_memory_fraction = 0.3
    session = tf.Session(config=config)
    keras.backend.set_session(session)
    return session


class OperatorServicer(vggrpc.rpc_pb2_grpc.OperatorServicer):
    def __init__(self):
        self.session = keras_config()
        self.vgg_ins = Vgg()

    def Execute(self, request, context):
        logging.info("execute")
        grpc_vectors = []
        with self.session.as_default():
            with self.session.graph.as_default():
                vectors = run(self.vgg_ins, request.datas, request.urls)
                for vector in vectors:
                    v = vggrpc.rpc_pb2.Vector(element=vector)
                    grpc_vectors.append(v)
                return vggrpc.rpc_pb2.ExecuteReply(nums=len(vectors),
                                                   vectors=grpc_vectors,
                                                   metadata=[])

    def Healthy(self, request, context):
        logging.info("healthy")
        return vggrpc.rpc_pb2.HealthyReply(healthy="healthy")

    def Identity(self, request, context):
        logging.info("identity")
        vgg = self.vgg_ins
        return vggrpc.rpc_pb2.IdentityReply(name=vgg.name,
                                            endpoint=ENDPOINT,
                                            type=vgg.type,
                                            input=vgg.input,
                                            output=vgg.output,
                                            dimension=vgg.dimension,
                                            metricType=vgg.metric_type)


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    vggrpc.rpc_pb2_grpc.add_OperatorServicer_to_server(OperatorServicer(), server)
    server.add_insecure_port('[::]:%s' % port)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter)
    port = ENDPOINT.split(":")[-1]
    logging.info("Start server")
    serve(port)
