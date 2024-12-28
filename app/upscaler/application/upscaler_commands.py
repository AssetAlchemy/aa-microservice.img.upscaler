from upscaler.domain.upscaler_service import UpscalerService


class Upscale2x:
    def __init__(self, upscaler_service: UpscalerService):
        self.upscaler_service = upscaler_service

    def execute(self, image_bytes: bytes) -> bytes:
        return self.upscaler_service.upscale_2x(image_bytes)


class Upscale4x:
    def __init__(self, upscaler_service: UpscalerService):
        self.upscaler_service = upscaler_service

    def execute(self, image_bytes: bytes) -> bytes:
        return self.upscaler_service.upscale_4x(image_bytes)
