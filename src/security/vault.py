"""
Security Vault Module
Mã hóa và giải mã API Keys sử dụng thư viện cryptography (Fernet - Symmetric encryption).
"""
import os
from cryptography.fernet import Fernet
from typing import Optional

class Vault:
    def __init__(self, key: Optional[bytes] = None):
        # Security Note: Khóa mã hóa phải được tiêm từ biến môi trường ngoài, 
        # tuyệt đối KHÔNG hardcode trong mã nguồn (Tuân thủ Governance Rule #01).
        self.key = key or os.environ.get("NPO_MASTER_KEY", "").encode()
        if not self.key:
            raise ValueError("Master key is missing. Set NPO_MASTER_KEY environment variable.")
        self.cipher = Fernet(self.key)

    def encrypt_api_key(self, api_key: str) -> bytes:
        """
        Mã hóa API key thành chuỗi bytes an toàn.
        
        Bản chất Security: Fernet sử dụng thuật toán AES-128 ở chế độ CBC (Cipher Block Chaining)
        kết hợp với chữ ký SHA256 HMAC (Hash-based Message Authentication Code) để đảm bảo toàn vẹn dữ liệu.
        Điều này ngăn chặn kẻ tấn công vừa không thể đọc được key, vừa không thể thay đổi nội dung (tampering)
        mà không bị phát hiện vì chữ ký HMAC sẽ không khớp. Điều này còn được gọi là Authenticated Encryption.
        """
        return self.cipher.encrypt(api_key.encode('utf-8'))

    def decrypt_api_key(self, encrypted_key: bytes) -> str:
        """Giải mã API key."""
        return self.cipher.decrypt(encrypted_key).decode('utf-8')

    @staticmethod
    def generate_key() -> bytes:
        """Tạo khóa mới. Chỉ dùng một lần khi khởi tạo hệ thống."""
        return Fernet.generate_key()
