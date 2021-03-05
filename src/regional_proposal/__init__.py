from abc import ABC, abstractmethod


class BaseRegionalProposal(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_iou(self, b1, b2):
        """Compute the iou of 2 bboxes"""
        pass

    @abstractmethod
    def remove_overlap_rp(self, bboxes, threshold):
        """Remove rp with IoU > threshold"""
        pass

    @abstractmethod
    def get_bboxes(self, image):
        """Get bounding boxes from algorithm"""
        pass

    @abstractmethod
    def draw_bboxes(self, image, bboxes, seed):
        """Draw bounding boxes on top of image"""
        pass

    @abstractmethod
    def get_cropped_rps(self, image, bboxes):
        """Get cropped rp from image"""
        pass
