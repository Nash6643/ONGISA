from forge_api.webhooks import verify_github_signature

def test_verify_github_signature_valid():
    secret = "my_secret"
    body = b"hello world"
    # Calculated sha256 for 'hello world' with secret 'my_secret'
    sig = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify_github_signature(secret, body, sig) is True