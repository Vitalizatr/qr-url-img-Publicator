import io
import base64
import qrcode


class QrCoder: 
    def __init__(self, box_size: int = 10, border: int = 4):
        self.qr = qrcode.QRCode(
            
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )

    def url_to_qr(self, url: str) -> str: 
        if url is None or len(url) > 100: 
            raise ValueError("Invalid URL: Link is empty or exceeds 100 characters")
        
        try:
            self.qr.add_data(url)
            self.qr.make(fit=True)  
            img = self.qr.make_image()
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            binary_data = buffer.getvalue()
        
            base64_bytes = base64.b64encode(binary_data)

            base64_string = base64_bytes.decode("utf-8")

            return base64_string
        finally:
            self.qr.clear()
