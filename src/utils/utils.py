import cv2
import matplotlib.pyplot as plt


def draw_bboxes(image, bboxes):
    for box in bboxes:
        res = cv2.rectangle(
            image,
            (box[0], box[1]),
            (box[0] + box[2], box[1] + box[3]),
            (128, 0, 0),
            2,
        )
    return res


def draw_digits(image, bboxes, labels, return_res=False):
    for box, label in zip(bboxes, labels):
        res = cv2.rectangle(
            image,
            (box[0], box[1]),
            (box[0] + box[2], box[1] + box[3]),
            (128, 0, 0),
            1,
        )
        res = cv2.putText(
            res,
            str(label),
            (box[0], box[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 0),
            1,
        )
    if return_res:
        return res
    else:
        fig = plt.figure(figsize=(8, 8))
        plt.axis("off")
        plt.imshow(res)


def remove_overlapped_bboxes(bboxes):

    res = []
    bboxes.sort(key=(lambda x: x[2] * x[3]))
    for bbox in bboxes:
        if not res:
            res.append(bbox)
        else:
            overlapped = False
            for rp in res:
                if if_overlapped(bbox, rp):
                    overlapped = True
                    break
            if not overlapped:
                res.append(bbox)

    return res


def if_overlapped(b1, b2):

    b1_area = b1[2] * b1[3]
    b2_area = b2[2] * b2[3]

    inter_height = max(0, min(b1[1] + b1[3], b2[1] + b2[3]) - max(b1[1], b2[1]))
    inter_width = max(0, min(b1[0] + b1[2], b2[0] + b2[2]) - max(b1[0], b2[0]))
    inter_area = inter_height * inter_width
    if inter_area == b1_area or inter_area == b2_area:
        return True
    else:
        return False
