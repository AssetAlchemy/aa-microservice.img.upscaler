class UpscalerService:
    def upscale_2x(self, img_bytes: bytes) -> bytes:
        raise NotImplementedError()

    def upscale_4x(self, img_bytes: bytes) -> bytes:
        raise NotImplementedError()
