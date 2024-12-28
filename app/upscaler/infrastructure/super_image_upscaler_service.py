import time
from numbers import Number
from io import BytesIO

import torch
from PIL import Image
from super_image import EdsrModel, ImageLoader

from upscaler.domain.upscaler_service import UpscalerService


class SuperImageUpscalerService(UpscalerService):
    def __init__(self):
        self.model = "eugenesiow/edsr-base"

    def _tensor_to_bytes(self, preds: torch.Tensor) -> bytes:
        preds = preds.squeeze(0).permute(1, 2, 0).cpu().detach().numpy()

        image = Image.fromarray((preds * 255).astype("uint8"))

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        return buffer.getvalue()

    def _upscale(self, img_bytes: bytes, scale: Number) -> bytes:
        image = Image.open(BytesIO(img_bytes)).convert("RGB")
        model = EdsrModel.from_pretrained(self.model, scale=scale)
        inputs = ImageLoader.load_image(image)

        start_time = time.time()

        preds = model(inputs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"El tiempo transcurrido es {elapsed_time} segundos.")

        image_bytes = self._tensor_to_bytes(preds)

        return image_bytes

    def upscale_2x(self, img_bytes: bytes) -> bytes:
        return self._upscale(img_bytes=img_bytes, scale=2)

    def upscale_4x(self, img_bytes: bytes) -> bytes:
        return self._upscale(img_bytes=img_bytes, scale=4)
