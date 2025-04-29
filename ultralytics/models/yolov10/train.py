import sys
import os
# 项目视频讲解：https://www.bilibili.com/video/BV1Gr421L7Ug/?spm_id_from=333.999.0.0
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.append(r"D:\Codes\yolov10-main\ultralytics\models\yolov10")
from ultralytics.models.yolo.detect import DetectionTrainer
from ultralytics.models.yolov10.val import YOLOv10DetectionValidator
from ultralytics.models.yolov10.model import YOLOv10DetectionModel
from copy import copy
from ultralytics.utils import RANK

class YOLOv10DetectionTrainer(DetectionTrainer):
    def get_validator(self):
        """Returns a DetectionValidator for YOLO model validation."""
        self.loss_names = "box_om", "cls_om", "dfl_om", "box_oo", "cls_oo", "dfl_oo", 
        return YOLOv10DetectionValidator(
            self.test_loader, save_dir=self.save_dir, args=copy(self.args), _callbacks=self.callbacks
        )

    def get_model(self, cfg=None, weights=None, verbose=True):
        """Return a YOLO detection model."""
        model = YOLOv10DetectionModel(cfg, nc=self.data["nc"], verbose=verbose and RANK == -1)
        if weights:
            model.load(weights)
        return model
