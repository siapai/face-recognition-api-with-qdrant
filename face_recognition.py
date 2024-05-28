# insight face
import os

from insightface.app import FaceAnalysis
import numpy as np
import pandas as pd
import cv2

# configure face analysis
faceapp = FaceAnalysis(name='buffalo_sc', root='insightface_model', providers=['CPUExecutionProvider'])
faceapp.prepare(ctx_id=0, det_size=(640, 640), det_thresh=0.5)


class PersonRegistration:
    # noinspection PyMethodMayBeStatic
    def get_embedding(self, company, username, file):
        embedding = None
        path = f"./persons/{company}/{username}/{file}"
        print(f"reading... {path}")
        img_arr = cv2.imread(path)
        results = faceapp.get(img_arr, max_num=1)
        if len(results) > 0:
            result = results[0]
            embedding = result["embedding"]
        return embedding
