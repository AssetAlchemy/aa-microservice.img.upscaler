from numbers import Number
from io import BytesIO
import warnings

import time

import torch
from PIL import Image
from py_real_esrgan.model import RealESRGAN

from upscaler.domain.upscaler_service import UpscalerService


class PyRealEsrganUpscalerService(UpscalerService):
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        warnings.simplefilter("ignore", category=FutureWarning)

    def _get_model(self, scale: Number):
        models = {
            "2": "weights/realesr-general-x2v3.pth",
            "4": "weights/realesr-general-x4v3.pth",
        }
        return models.get(str(scale))

    def _upscale(self, img_bytes: bytes, scale: Number) -> bytes:
        image = Image.open(BytesIO(img_bytes)).convert("RGB")

        model = RealESRGAN(self.device, scale=scale)
        model.load_weights(self._get_model(scale), download=True)

        start_time = time.time()

        sr_image = model.predict(image)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"El tiempo transcurrido es {elapsed_time} segundos.")

        img_byte_arr = BytesIO()
        sr_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        return img_byte_arr.getvalue()

    def upscale_2x(self, img_bytes: bytes) -> bytes:
        return self._upscale(img_bytes=img_bytes, scale=2)

    def upscale_4x(self, img_bytes: bytes) -> bytes:
        return self._upscale(img_bytes=img_bytes, scale=4)
