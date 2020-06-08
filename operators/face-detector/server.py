import os
import logging
import grpc
from concurrent import futures
import rpc.rpc_pb2
import rpc.rpc_pb2_grpc
from face_detector import run, MTCNNDetectFace as Detector

ENDPOINT = os.getenv("OP_ENDPOINT", "127.0.0.1:50005")


class OperatorServicer(rpc.rpc_pb2_grpc.OperatorServicer):
    def __init__(self):
        self.detector = Detector()

    def Execute(self, request, context):
        logging.info("execute")
        grpc_metas = []
        result_images = run(self.detector, request.datas, request.urls)
        for result_image in result_images[0]:
            meta = rpc.rpc_pb2.MetaData(data = result_image.encode())
            grpc_metas.append(meta)
        return rpc.rpc_pb2.ExecuteReply(nums=len(grpc_metas),
                                        vectors=[],
                                        metadata=grpc_metas)

    def Healthy(self, request, context):
        logging.info("healthy")
        return rpc.rpc_pb2.HealthyReply(healthy="healthy")

    def Identity(self, request, context):
        logging.info("identity")

        encoder = self.detector
        return rpc.rpc_pb2.IdentityReply(name=encoder.name,
                                         endpoint=ENDPOINT,
                                         type=encoder.type,
                                         input=encoder.input,
                                         output=encoder.output,
                                         dimension=encoder.dimension,
                                         metricType=encoder.metric_type)


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
