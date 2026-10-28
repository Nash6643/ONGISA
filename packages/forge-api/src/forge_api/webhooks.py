import hmac
import hashlib

def verify_github_signature(secret: str, payload_body: bytes, signature_header: str) -> bool:
    if not signature_header:
        return False
    sha_name, signature = signature_header.split('=')
    if sha_name != 'sha256':
        return False
    mac = hmac.new(secret.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)