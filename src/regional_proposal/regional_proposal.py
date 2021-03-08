"""Regional proposal"""

import random

import cv2
import numpy as np
import matplotlib.pyplot as plt
import selective_search as ss

from src.regional_proposal import BaseRegionalProposal


class RpMser(BaseRegionalProposal):
    """Regional proposal MSER algorithm"""

    def __init__(self, name="MSER", thickness=2):
        super().__init__(name)
        self.rp = cv2.MSER_create()
        self.thickness = thickness

    def get_iou(self, b1, b2):

        inter_height = max(0, min(b1[1] + b1[3], b2[1] + b2[3]) - max(b1[1], b2[1]))
        inter_width = max(0, min(b1[0] + b1[2], b2[0] + b2[2]) - max(b1[0], b2[0]))
        inter_area = inter_height * inter_width
        b1_area = b1[2] * b1[3]
        b2_area = b2[2] * b2[3]
        iou = round(inter_area / (b1_area + b2_area - inter_area), 3)

        return iou

    def remove_overlap_rp(self, bboxes, threshold=0.5):
        """Remove rp from MSER with IoU > threshold"""

        res = []
        for box in bboxes:
            area = box[2] * box[3]
            # Disgard rp if it is too large
            if area >= 100 * 100:
                continue

            # Disgard rp if it is too small
            if box[2] < 10 or box[3] < 10:
                continue

            if not res:
                res.append(box)
            else:
                duplicate = False
                for rp in res:
                    iou = self.get_iou(box, rp)
                    if iou > threshold:
                        duplicate = True
                        break
                if not duplicate:
                    res.append(box)
        return res

    def draw_bboxes(self, image, bboxes, seed=42, return_res=False):

        seed = hash(str(seed))
        random.seed(seed)
        if len(list(image.shape)) == 3:
            color = [
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for _ in range(len(bboxes))
            ]
        else:
            color = [(128, 0, 0) for _ in range(len(bboxes))]

        res = image.copy()
        for index, box in enumerate(bboxes):

            res = cv2.rectangle(
                image,
                (box[0], box[1]),
                (box[0] + box[2], box[1] + box[3]),
                color[index],
                self.thickness,
            )

        if return_res:
            return res
        else:
            fig = plt.figure(figsize=(8, 8))
            plt.axis("off")
            plt.imshow(res)

    def get_bboxes(self, image, threshold=None):
        _, bboxes = self.rp.detectRegions(image)
        if threshold is not None:
            bboxes = self.remove_overlap_rp(bboxes, threshold)
        return bboxes

    def get_cropped_rps(self, image, bboxes):

        rp = []
        # Crop bounding boxes
        for box in bboxes:
            rp.append(image[box[1] : box[1] + box[3], box[0] : box[0] + box[2]])

        return rp


class RpSelectiveSearch(BaseRegionalProposal):
    """Regional proposal Selective Search algorithm"""

    def __init__(self, name="Selective Search", mode="fast"):
        super().__init__(name)
        self.mode = mode
        self.rp = ss.selective_search

    def get_iou(self, b1, b2):

        inter_area = (min(b1[2], b2[2]) - max(b1[0], b2[0])) * (
            min(b1[3], b2[3]) - (max(b1[1], b2[1]))
        )
        b1_area = (b1[2] - b1[0]) * (b1[3] - b1[1])
        b2_area = (b2[2] - b2[0]) * (b2[3] - b2[1])
        iou = round(inter_area / (b1_area + b2_area - inter_area), 3)

        return iou

    def remove_overlap_rp(self, bboxes, threshold=0.5):

        res = []
        for box in bboxes:
            area = (box[2] - box[0]) * (box[3] - box[1])
            # Disgard rp if it is too large
            if area >= 100 * 100:
                continue

            # Disgard rp if it is too small
            if (box[2] - box[0]) < 10 or (box[3] - box[1]) < 10:
                continue

            if not res:
                res.append(box)
            else:
                duplicate = False
                for rp in res:
                    iou = self.get_iou(box, rp)
                    if iou > threshold:
                        duplicate = True
                        break
                if not duplicate:
                    res.append(box)
        return res

    def draw_bboxes(self, image, bboxes, seed=42, return_res=False):

        thickness = 2
        seed = hash(str(seed))
        random.seed(seed)
        if len(list(image.shape)) == 3:
            color = [
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for _ in range(len(bboxes))
            ]
        else:
            color = [(128, 0, 0) for _ in range(len(bboxes))]

        for index, box in enumerate(bboxes):

            res = cv2.rectangle(
                image,
                (box[0], box[1]),
                (box[2], box[3]),
                color[index],
                thickness,
            )
        if return_res:
            return res
        else:
            fig = plt.figure(figsize=(8, 8))
            plt.axis("off")
            plt.imshow(image)

    def get_bboxes(self, image, threshold=None):

        _, bboxes = self.rp(image, model=self.mode)
        if threshold is not None:
            bboxes = self.remove_overlap_rp(bboxes, threshold)
        return bboxes

    def get_cropped_rps(self, image, bboxes):

        rp = []
        # Crop bounding boxes
        for box in bboxes:
            rp.append(image[box[1] : box[3], box[0] : box[2]])

        return rp
