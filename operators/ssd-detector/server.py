import os
import logging
import grpc
from concurrent import futures
import rpc.rpc_pb2
import rpc.rpc_pb2_grpc
from ssd import run, SSDDetectObject as Detector

ENDPOINT = os.getenv("OP_ENDPOINT", "127.0.0.1:80")


class OperatorServicer(rpc.rpc_pb2_grpc.OperatorServicer):
    def __init__(self):
        self.detector = Detector()

    def Execute(self, request, context):
        logging.info("execute")
        grpc_metas = []
        result_images = run(self.detector, request.datas, request.urls)
        # just for test, need adjust proto
        logging.info('len of result images： %d', len(result_images))
        result_images = result_images[0]

        for result_image in result_images:
            data = rpc.rpc_pb2.MetaData(data=bytes(result_image, encoding='utf-8'))
            grpc_metas.append(data)
        return rpc.rpc_pb2.ExecuteReply(nums=len(grpc_metas),
                                        vectors=[],
                                        metadata=grpc_metas)

    def Healthy(self, request, context):
        logging.info("healthy")
        return rpc.rpc_pb2.HealthyReply(healthy="healthy")

    def Identity(self, request, context):
        logging.info("identity")
        detector = self.detector
        return rpc.rpc_pb2.IdentityReply(name=detector.name,
                                         endpoint=ENDPOINT,
                                         type=detector.type,
                                         input=detector.input,
                                         output=detector.output,
                                         dimension=detector.dimension,
                                         metricType=detector.metric_type)


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
