from operators.mtcnn_detect_face import MTCNNDetectFace
from operators.face_embedding import EmbedFaces
from operators.gender_embedding import DetectGender
from operators.ssd import SSDDetectObject

import cv2


def face():
    # img_path = "/tmp/test.png"
    img_path = "/home/abner/Desktop/test1.jpg"
    image = cv2.imread(img_path)
    detector = MTCNNDetectFace()
    images = detector.bulk_execute([image])
    print(images)

    gender_detector = DetectGender()
    res = gender_detector.bulk_execute(images[0])
    # res = gender_detector.execute(images[0][0])
    print(res)

    # age_detector = DetectAge()
    # res = age_detector.execute(image, bboxes[0])
    # print(res)

    encoder = EmbedFaces()
    encoder.fetch_resources()
    # res = encoder.execute(images[0][0])
    res = encoder.bulk_execute(images[0])
    print(res)


def object():
    img_path = "/home/abner/Desktop/test8.jpg"
    image = cv2.imread(img_path)
    detector = SSDDetectObject()
    res = detector.execute([image])
    print(res)

if __name__ == "__main__":
    face()
    # object()