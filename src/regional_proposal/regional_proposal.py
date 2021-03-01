"""Regional proposal"""

import cv2
import numpy as np


def get_rp_from_mser(img):
    """Obtain regional proposals from MSER algorithm"""

    # Convert the image into grayscale.
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply MSER to get bounding boxes
    mser_ = cv2.MSER_create()
    _, bboxes = mser_.detectRegions(img)
    bboxes = np.unique(bboxes, axis=0)
    bboxes = remove_overlap_rp(bboxes)

    rp = []
    # Crop bounding boxes
    for box in bboxes:
        rp.append(img[box[1] : box[1] + box[3], box[0] : box[0] + box[2]])

    return rp


def remove_overlap_rp(bboxes, threshold=0.9):
    """Remove rp is IoU > threshold"""

    res = []
    for box in bboxes:

        # Disgard rp if it is too large
        area = box[2] * box[3]
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
                iou = get_iou(box, rp)
                if iou > threshold:
                    duplicate = True
                    break
            if not duplicate:
                res.append(box)
    return res


def get_iou(b1, b2):
    """Compute the IoU of 2 boxes"""

    inter_area = (min(b1[1] + b1[3], b2[1] + b2[3]) - max(b1[1], b2[1])) * (
        min(b1[0] + b1[2], b2[0] + b2[2]) - max(b1[0], b2[0])
    )
    b1_area = b1[2] * b1[3]
    b2_area = b2[2] * b2[3]

    iou = round(inter_area / (b1_area + b2_area - inter_area), 3)

    return iou
