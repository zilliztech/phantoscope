import logging
from typing import List
from models.pipeline import Pipeline as DB
from models.pipeline import insert_pipeline
from models.pipeline import search_pipeline
from models.pipeline import del_pipeline
from models.pipeline import update_pipeline
from common.error import PipelineCheckError
from common.error import PipelineIlegalError
from common.error import RPCExecError
from common.error import NotExistError
from common.const import OPERATOR_TYPE_ENCODER
from common.const import OPERATOR_TYPE_PROCESSOR
from operators.operator import all_operators
from operators.operator import operator_detail
from operators.client import execute
from storage.storage import MilvusIns

logger = logging.getLogger(__name__)


class Pipeline():
    def __init__(self, name, input, output, dimension, index_file_size,
                 metric_type, description,
                 processors: List[str], encoder: str):
        self._pipeline_name = name
        self._input = input
        self._output = output
        self._dimension = dimension
        self._index_file_size = index_file_size
        self._metric_type = metric_type
        self._pipeline_description = description
        self._processors = processors
        self._encoder = encoder
        self._description = description

    @property
    def name(self):
        return self._pipeline_name

    @property
    def description(self):
        return self._pipeline_description

    @property
    def dimension(self):
        return self._dimension

    @property
    def metric_type(self):
        return self._metric_type

    @property
    def index_file_size(self):
        return self._index_file_size

    @property
    def processors(self):
        return self._processors

    @processors.setter
    def processors(self, processors):
        self._processors = processors

    @property
    def encoder(self):
        return self._encoder

    @encoder.setter
    def encoder(self, encoder):
        self._encoder = encoder

    def save(self):
        p = DB(name=self._pipeline_name, input=self._input,
               output=self._output, dimension=self._dimension,
               index_file_size=self._index_file_size,
               metric_type=self._metric_type,
               processors=",".join(self._processors),
               encoder=self._encoder, description=self._description)
        try:
            insert_pipeline(p)
        except Exception as e:
            raise e
        return self


def all_pipelines():
    res = []
    try:
        pipelines = search_pipeline()
        for p in pipelines:
            pipe = Pipeline(name=p.Pipeline.name, input=p.Pipeline.input,
                            output=p.Pipeline.output, dimension=p.Pipeline.dimension,
                            index_file_size=p.Pipeline.index_file_size,
                            metric_type=p.Pipeline.metric_type,
                            description=p.Pipeline.description,
                            processors=p.Pipeline.processors.split(","),
                            encoder=p.Pipeline.encoder)
            res.append(pipe)
        return res
    except Exception as e:
        logger.error(e)
        return e


def _all_pipelines():
    res = []
    try:
        pipelines = search_pipeline()
        for p in pipelines:
            pipe = Pipeline(name=p.Pipeline.name, input=p.Pipeline.input,
                            output=p.Pipeline.output, dimension=p.Pipeline.dimension,
                            index_file_size=p.Pipeline.index_file_size,
                            metric_type=p.Pipeline.metric_type,
                            description=p.Pipeline.description,
                            processors=p.Pipeline.processors.split(","),
                            encoder=p.Pipeline.encoder)
            res.append(pipe)
        return res
    except Exception as e:
        raise e


def pipeline_detail(name):
    try:
        p = search_pipeline(name)
        if not p:
            raise NotExistError("pipeline %s is not exist" % name, "")
        if not p.processors:
            pr = []
        else:
            pr = p.processors.split(",")
        pipe = Pipeline(name=p.name, input=p.input,
                        output=p.output, dimension=p.dimension,
                        index_file_size=p.index_file_size,
                        metric_type=p.metric_type,
                        description=p.description,
                        processors=pr,
                        encoder=p.encoder)
        return pipe
    except Exception as e:
        return e


def new_pipeline(name, input, index_file_size, processors, encoder, description=None):
    try:
        encoder = operator_detail(encoder)
        pipe = Pipeline(name=name, input=input, output=encoder.output, dimension=encoder.dimension,
                        index_file_size=index_file_size, metric_type=encoder.metric_type,
                        description=description,
                        processors=processors.split(","), encoder=encoder.name)
        if pipeline_ilegal(pipe):
            return PipelineIlegalError("Pipeline ilegal check error", "")
        milvus_collection_name = f"{name}_{encoder.name}"
        MilvusIns.new_milvus_collection(milvus_collection_name, encoder.dimension, index_file_size, encoder.metric_type)
        return pipe.save()
    except Exception as e:
        print(e)
        logger.error(e)
        return e


def delete_pipeline(name):
    try:
        p = del_pipeline(name)
        if not p:
            raise NotExistError("pipeline %s is not exist" % name, "")
        p = p[0]
        milvus_collection_name = f"{name}_{p.encoder}"
        MilvusIns.del_milvus_collection(milvus_collection_name)
        pipe = Pipeline(name=p.name, input=p.input,
                        output=p.output, dimension=p.dimension,
                        index_file_size=p.index_file_size,
                        metric_type=p.metric_type,
                        description=p.description,
                        processors=p.processors.split(","),
                        encoder=p.encoder)
        return pipe
    except Exception as e:
        logger.error(e)
        return e


def run_pipeline(p, **kwargs):
    todo_list = []
    if not isinstance(p, Pipeline):
        raise PipelineCheckError("check pipeline with error", "%s is not a Pipeline instance" % p)
    operators = all_operators()
    processor_operators = {x.name: x for x in operators if x.type == OPERATOR_TYPE_PROCESSOR}
    encoder_operators = {x.name: x for x in operators if x.type == OPERATOR_TYPE_ENCODER}
    for i in p.processors:
        if i not in processor_operators:
            raise PipelineCheckError("processors not exist", "%s not exist in supported processors " % i)
        todo_list.append(processor_operators[i])
    if p.encoder not in encoder_operators:
        raise PipelineCheckError("encoder not exist", "%s not exist in supported encoders" % p.encoder)
    todo_list.append(encoder_operators[p.encoder])

    def runner(todo_list):
        metadata, vectors = [], []
        urls = [kwargs['url']] if kwargs['url'] else []
        datas = [kwargs['data']] if kwargs['data'] else []
        try:
            for i in todo_list:
                if i.type == "processor":
                    _, metadatas = execute(i, urls=urls, datas=datas)
                    urls = [x.url for x in metadatas]
                    datas = [x.metadata for x in metadatas]
                if i.type == "encoder":
                    vectors, _ = execute(i, urls=urls, datas=datas)
                    return vectors
            return metadata
        except Exception as e:
            raise RPCExecError("Execute with error", e)
    try:
        return runner(todo_list)
    except Exception as e:
        logger.error(e)
        raise e


def pipeline_ilegal(pipe):
    registed_operators = [x for x in all_operators() if x.type == OPERATOR_TYPE_ENCODER]
    for op in registed_operators:
        if pipe.encoder == op.name:
            if pipe.dimension == op.dimension and pipe.metric_type == op.metric_type:
                return False
    return True
