from application.application import application_detail
from application.mapping import new_mapping_ins
from pipeline.pipeline import pipeline_detail, run_pipeline
from common.error import NotExistError
from common.error import NoneVectorError
from storage.storage import MilvusIns
from models.mapping import search_ids_from_mapping, search_from_mapping


def search(name, fields={}, topk=10, nprobe=16):
    res = []
    try:
        app = application_detail(name)
#        accept_fields = [x for x, y in app.fields.items() if y.get('type') != "object"]
        pipeline_fields = {x: y['pipeline'] for x, y in app.fields.items() if y.get('type') == "object"}
        for n, p in pipeline_fields.items():
            pipe = pipeline_detail(p)
            value = fields.get(n)
            file_data = value.get('data')
            url = value.get('url')
            vectors = run_pipeline(pipe, data=file_data, url=url)
            if not vectors:
                raise NoneVectorError("can't encode data by encoder, check input or encoder", "")
            milvus_collection_name = f"{pipe.name}_{pipe.encoder}"
            vids = MilvusIns.search_vectors(milvus_collection_name, vectors, topk=topk, nprobe=nprobe)
            # here add scoreling function
            dbs = search_ids_from_mapping([x.id for x in vids[0]])
            for db in dbs:
                m = new_mapping_ins(id=db.id, app_name=db.app_name,
                                    image_url=db.image_url, fields=db.fields,
                                    target_fields=db.target_fields)
                res.append(m)
        return res
    except Exception as e:
        return e
