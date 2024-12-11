import os
import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

key_file_path = "encrypted_key.bin"

# 生成对称密钥
def generate_key():
    return Fernet.generate_key()

# 使用口令加密密钥
def encrypt_key(key, password):
    # 生成盐
    salt = os.urandom(16)

    # 使用 PBKDF2HMAC 派生密钥
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    # 派生密钥
    derived_key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

    # 使用派生密钥加密对称密钥
    fernet = Fernet(derived_key)
    encrypted_key = fernet.encrypt(key)
    return salt + encrypted_key  # 将盐和加密密钥一起返回


# 使用口令解密密钥
def decrypt_key(encrypted_key_with_salt, password):
    # 分离盐和加密密钥
    salt = encrypted_key_with_salt[:16]
    encrypted_key = encrypted_key_with_salt[16:]

    # 使用相同的 KDF 生成派生密钥
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    derived_key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

    # 使用派生密钥解密对称密钥
    fernet = Fernet(derived_key)

    try:
        decrypted_key = fernet.decrypt(encrypted_key)
        return decrypted_key
    except InvalidToken:
        return None

def get_key(password):
    decrypted_key = ""
    if not os.path.exists(key_file_path):
        key = generate_key()
        encrypted_key = encrypt_key(key, password)
        with open("encrypted_key.bin", "wb") as key_file:
            key_file.write(encrypted_key)
        return key
    else:
        with open(key_file_path, "rb") as key_file:
            key = key_file.read()
        decrypted_key = decrypt_key(key, password)
        return decrypted_key


def get_decrypt_key(key, password):
    decrypted_key = decrypt_key(key, password)
    return decrypted_key

def update_key(old_password, new_password):
    if not os.path.exists(key_file_path):
        return
    with open(key_file_path, "rb") as key_file:
        key = key_file.read()
    decrypted_key = decrypt_key(key, old_password)
    if decrypted_key is None:
        return None
    encrypted_key = encrypt_key(decrypted_key, new_password)
    with open(key_file_path, "wb") as key_file:
        key_file.write(encrypted_key)

# 主程序
if __name__ == "__main__":
    ps = input("input password: ")
    dk = get_key(ps)
    if dk is None:
        print("password is incorrect")
    else:
        print(f"key: {dk.decode()}")
    new_ps = input("input password: ")
    update_key(ps, new_ps)
