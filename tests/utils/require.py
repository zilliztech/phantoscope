import time
from functools import wraps
from operators.operator import register_operators, delete_operators, operator_detail
from pipeline.pipeline import create_pipeline, delete_pipeline
from application.application import new_application, delete_application


def pre_operator(name="pytest_op_1", type="encoder",
                 addr="psoperator/vgg16-encoder:latest", author="phantoscope",
                 version="0.1", description="test operator"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            register_operators(name=name, type=type, addr=addr, author=author,
                               version=version, description=description)
            func(*args, **kwargs)
            delete_operators(name=name)

        return wrapper

    return decorator


def pre_instance(operator_name="pytest_op_1", name="ins1"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            operator = operator_detail(operator_name)
            operator.new_instance(name)
            func(*args, **kwargs)
            operator.delete_instance(name)

        return wrapper

    return decorator


def pre_pipeline(name="pytest_pipe_1", processors="",
                 encoder={"name": "pytest_op_1", "instance": "ins1"},
                 description="test pipeline"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            create_pipeline(name=name, processors=processors, encoder=encoder)
            func(*args, **kwargs)
            delete_pipeline(name)

        return wrapper

    return decorator


def pre_application(name="pytest_app_1",
                    fields={"full": {"type": "pipeline", "value": "pytest_pipe_1"}},
                    s3_buckets="test_bucket"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(4)  # wait for opertaor instance start
            new_application(app_name=name, fields=fields, s3_buckets=s3_buckets)
            func(*args, **kwargs)
            delete_application(name)

        return wrapper

    return decorator


def sleep_time(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            func(*args, **kwargs)

        return wrapper

    return decorator
