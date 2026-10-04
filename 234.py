import base64
import hashlib
import hmac
import os
import sys
import urllib.parse

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305

# 嘗試載入線上翻譯套件（若未安裝則自動切換為內建詞庫模式）
try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False

# ----------------------------------------------------------------------
# 1. 加密與解密引擎 (16 項功能)
# ----------------------------------------------------------------------

class CryptoEngine:

    # 1. 凱撒密碼
    @staticmethod
    def caesar_cipher(text: str, shift: int, decrypt: bool = False) -> str:
        if decrypt:
            shift = -shift
        result = []
        for char in text:
            if char.isalpha():
                start = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - start + shift) % 26 + start))
            else:
                result.append(char)
        return "".join(result)

    # 2. 維吉尼亞密碼
    @staticmethod
    def vigenere_cipher(text: str, key: str, decrypt: bool = False) -> str:
        if not key:
            return text
        key = key.upper()
        result = []
        key_idx = 0
        for char in text:
            if char.isalpha():
                shift = ord(key[key_idx % len(key)]) - ord('A')
                if decrypt:
                    shift = -shift
                start = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - start + shift) % 26 + start))
                key_idx += 1
            else:
                result.append(char)
        return "".join(result)

    # 3. 培根密碼
    @staticmethod
    def baconian_encode(text: str) -> str:
        bacon_map = {chr(i + 65): f"{i:05b}".replace('0', 'A').replace('1', 'B') for i in range(26)}
        return " ".join([bacon_map.get(c.upper(), c) for c in text if c.isalpha()])

    @staticmethod
    def baconian_decode(text: str) -> str:
        reverse_map = {f"{i:05b}".replace('0', 'A').replace('1', 'B'): chr(i + 65) for i in range(26)}
        tokens = text.upper().split()
        res = []
        for token in tokens:
            if token in reverse_map:
                res.append(reverse_map[token])
            else:
                res.append(token)
        return "".join(res)

    # 4. Atbash 密碼
    @staticmethod
    def atbash_cipher(text: str) -> str:
        result = []
        for char in text:
            if 'A' <= char <= 'Z':
                result.append(chr(ord('Z') - (ord(char) - ord('A'))))
            elif 'a' <= char <= 'z':
                result.append(chr(ord('z') - (ord(char) - ord('a'))))
            else:
                result.append(char)
        return "".join(result)

    # 5. Base32
    @staticmethod
    def base32_encode(text: str) -> str:
        return base64.b32encode(text.encode('utf-8')).decode('utf-8')

    @staticmethod
    def base32_decode(encoded_str: str) -> str:
        return base64.b32decode(encoded_str.encode('utf-8')).decode('utf-8')

    # 6. Base85
    @staticmethod
    def base85_encode(text: str) -> str:
        return base64.b85encode(text.encode('utf-8')).decode('utf-8')

    @staticmethod
    def base85_decode(encoded_str: str) -> str:
        return base64.b85decode(encoded_str.encode('utf-8')).decode('utf-8')

    # 7. Hex 編碼/解碼
    @staticmethod
    def hex_encode(text: str) -> str:
        return text.encode('utf-8').hex()

    @staticmethod
    def hex_decode(hex_str: str) -> str:
        return bytes.fromhex(hex_str).decode('utf-8')

    # 8. URL Percent Encoding
    @staticmethod
    def url_encode(text: str) -> str:
        return urllib.parse.quote(text)

    @staticmethod
    def url_decode(text: str) -> str:
        return urllib.parse.unquote(text)

    # 9. AES-GCM 加密/解密
    @staticmethod
    def aes_gcm_encrypt(plaintext: str, key_str: str) -> str:
        key = hashlib.sha256(key_str.encode('utf-8')).digest()
        nonce = os.urandom(12)
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
        return base64.b64encode(nonce + ciphertext).decode('utf-8')

    @staticmethod
    def aes_gcm_decrypt(b64_data: str, key_str: str) -> str:
        key = hashlib.sha256(key_str.encode('utf-8')).digest()
        raw = base64.b64decode(b64_data)
        nonce, ciphertext = raw[:12], raw[12:]
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')

    # 10. ChaCha20-Poly1305 加密/解密
    @staticmethod
    def chacha20_encrypt(plaintext: str, key_str: str) -> str:
        key = hashlib.sha256(key_str.encode('utf-8')).digest()
        nonce = os.urandom(12)
        chacha = ChaCha20Poly1305(key)
        ciphertext = chacha.encrypt(nonce, plaintext.encode('utf-8'), None)
        return base64.b64encode(nonce + ciphertext).decode('utf-8')

    @staticmethod
    def chacha20_decrypt(b64_data: str, key_str: str) -> str:
        key = hashlib.sha256(key_str.encode('utf-8')).digest()
        raw = base64.b64decode(b64_data)
        nonce, ciphertext = raw[:12], raw[12:]
        chacha = ChaCha20Poly1305(key)
        return chacha.decrypt(nonce, ciphertext, None).decode('utf-8')

    # 11. SHA3-256 雜湊
    @staticmethod
    def sha3_256_hash(text: str) -> str:
        return hashlib.sha3_256(text.encode('utf-8')).hexdigest()

    # 12. HMAC-SHA256 簽名生成
    @staticmethod
    def generate_hmac(message: str, secret_key: str) -> str:
        return hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

    # 13. PBKDF2 密碼雜湊
    @staticmethod
    def pbkdf2_hash(password: str, salt_str: str = "default_salt") -> str:
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_str.encode('utf-8'), 100000)
        return key.hex()

    # 14. BLAKE2b 雜湊
    @staticmethod
    def blake2b_hash(text: str) -> str:
        return hashlib.blake2b(text.encode('utf-8')).hexdigest()

    # 15. RSA 公私鑰對生成與非對稱加解密
    @staticmethod
    def rsa_demo_encrypt_decrypt(plaintext: str) -> tuple:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        ciphertext = public_key.encrypt(
            plaintext.encode('utf-8'),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        b64_cipher = base64.b64encode(ciphertext).decode('utf-8')
        decrypted = private_key.decrypt(
            ciphertext,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        ).decode('utf-8')
        return b64_cipher, decrypted

    # 16. RSA 數位簽名與驗證
    @staticmethod
    def rsa_demo_sign_verify(message: str) -> tuple:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        signature = private_key.sign(
            message.encode('utf-8'),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        b64_sig = base64.b64encode(signature).decode('utf-8')
        try:
            public_key.verify(
                signature,
                message.encode('utf-8'),
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            is_valid = True
        except Exception:
            is_valid = False
        return b64_sig, is_valid


# ----------------------------------------------------------------------
# 2. 多語言翻譯引擎 (含7種特定語言)
# ----------------------------------------------------------------------

class TranslationEngine:
    """多國語言翻譯/轉換引擎"""

    # ISO 語言代碼對照表
    LANG_MAP = {
        "1": ("zh-TW", "中文 (繁體)"),
        "2": ("en", "英文 (English)"),
        "3": ("din", "丁卡文 (Dinka)"),
        "4": ("jam", "牙買加方言 (Jamaican Patois)"),
        "5": ("sa", "梵文 (Sanskrit / 天城文)"),
        "6": ("ja", "日文 (日本語)"),
        "7": ("ko", "韓文 (한국어)")
    }

    # 離線/備用詞庫 (用於不支援的方言或離線環境)
    FALLBACK_DICT = {
        "din": {  # 丁卡文簡易對照 (Dinka)
            "hello": "Möđöng", "friend": "Mäth", "thank you": "Yin aca leec", 
            "good": "Apath", "water": "Piu", "peace": "Dör"
        },
        "jam": {  # 牙買加方言 (Jamaican Patois)
            "hello": "Whaa gwaan", "friend": "Bredren", "thank you": "Tanks",
            "good": "Irie", "everything is fine": "Everything irie", "food": "NYAM"
        },
        "sa": {   # 梵文 (Sanskrit)
            "hello": "Namo Namah (नमो नमः)", "thank you": "Danyavadah (धन्यवादः)",
            "peace": "Shanti (शान्तिः)", "friend": "Mitram (मित्रम्)"
        }
    }

    @classmethod
    def translate(cls, text: str, target_lang_code: str) -> str:
        target_iso, lang_name = cls.LANG_MAP.get(target_lang_code, ("en", "English"))
        
        # 1. 若安裝了 deep-translator，優先呼叫線上翻譯服務
        if HAS_TRANSLATOR:
            try:
                # 若為牙買加方言或特殊語系，先調用特定模型
                translator = GoogleTranslator(source='auto', target=target_iso)
                translated = translator.translate(text)
                return translated
            except Exception:
                pass  # 若線上翻譯失敗或語言代碼受限，流向備用方案

        # 2. 離線/特殊語言規則備用翻譯機制
        text_lower = text.lower().strip()
        if target_iso in cls.FALLBACK_DICT and text_lower in cls.FALLBACK_DICT[target_iso]:
            return cls.FALLBACK_DICT[target_iso][text_lower]

        # 3. 梵文天城文音譯示範 (Devanagari Scheme)
        if target_iso == "sa":
            sanskrit_map = {"namaste": "नमस्ते", "shanti": "शान्तिः", "om": "ॐ", "karma": "कर्म"}
            return sanskrit_map.get(text_lower, f"[梵文對照範例]: {text} (Sanskrit Transliteration)")

        return f"[翻譯提示]: 建議執行 `pip install deep-translator` 以啟用「{lang_name}」的線上完整機器翻譯服務。\n原始輸入: {text}"


# ----------------------------------------------------------------------
# 3. 互動式選單介面 (CLI)
# ----------------------------------------------------------------------

def main():
    crypto_engine = CryptoEngine()
    
    while True:
        print("\n" + "="*50)
        print("     16 項擴充加密解密 & 7 國語言翻譯整合系統     ")
        print("="*50)
        print(" 【加密與解密模組】")
        print("  [1] 凱撒密碼          [9]  AES-256-GCM 加密")
        print("  [2] 維吉尼亞密碼      [10] ChaCha20-Poly1305 加密")
        print("  [3] 培根密碼          [11] SHA3-256 雜湊")
        print("  [4] Atbash 密碼       [12] HMAC-SHA256 簽名")
        print("  [5] Base32 編解碼     [13] PBKDF2 密碼雜湊")
        print("  [6] Base85 編解碼     [14] BLAKE2b 雜湊")
        print("  [7] Hex 編解碼        [15] RSA 非對稱加解密")
        print("  [8] URL 編解碼        [16] RSA 數位簽名與驗章")
        print("--------------------------------------------------")
        print(" 【多語言翻譯模組】")
        print("  [17] 進入 7 國語言翻譯器 (中/英/丁卡/牙買加/梵/日/韓)")
        print("--------------------------------------------------")
        print("  [0] 退出系統")
        print("="*50)
        
        choice = input("請選擇功能項目 (0-17): ").strip()
        
        if choice == "0":
            print("\n系統已退出。")
            break
            
        elif choice in [str(i) for i in range(1, 17)]:
            # 處理加密解密 16 項邏輯
            if choice == "1":
                mode = input("1) 加密 2) 解密: ").strip()
                text = input("請輸入內容: ")
                shift = int(input("請輸入位移量 (預設3): ") or 3)
                print(f"結果: {crypto_engine.caesar_cipher(text, shift, decrypt=(mode == '2'))}")
            elif choice == "2":
                mode = input("1) 加密 2) 解密: ").strip()
                text = input("請輸入內容: ")
                key = input("請輸入金鑰: ")
                print(f"結果: {crypto_engine.vigenere_cipher(text, key, decrypt=(mode == '2'))}")
            elif choice == "3":
                mode = input("1) 編碼 2) 解碼: ").strip()
                text = input("請輸入內容: ")
                res = crypto_engine.baconian_encode(text) if mode == "1" else crypto_engine.baconian_decode(text)
                print(f"結果: {res}")
            elif choice == "4":
                text = input("請輸入內容: ")
                print(f"結果: {crypto_engine.atbash_cipher(text)}")
            elif choice == "5":
                mode = input("1) 編碼 2) 解碼: ").strip()
                text = input("請輸入內容: ")
                print(f"結果: {crypto_engine.base32_encode(text) if mode == '1' else crypto_engine.base32_decode(text)}")
            elif choice == "6":
                mode = input("1) 編碼 2) 解碼: ").strip()
                text = input("請輸入內容: ")
                print(f"結果: {crypto_engine.base85_encode(text) if mode == '1' else crypto_engine.base85_decode(text)}")
            elif choice == "7":
                mode = input("1) 編碼 2) 解碼: ").strip()
                text = input("請輸入內容: ")
                print(f"結果: {crypto_engine.hex_encode(text) if mode == '1' else crypto_engine.hex_decode(text)}")
            elif choice == "8":
                mode = input("1) 編碼 2) 解碼: ").strip()
                text = input("請輸入內容: ")
                print(f"結果: {crypto_engine.url_encode(text) if mode == '1' else crypto_engine.url_decode(text)}")
            elif choice == "9":
                mode = input("1) 加密 2) 解密: ").strip()
                text = input("請輸入內容: ")
                pwd = input("請輸入自訂金鑰/密碼: ")
                res = crypto_engine.aes_gcm_encrypt(text, pwd) if mode == "1" else crypto_engine.aes_gcm_decrypt(text, pwd)
                print(f"結果: {res}")
            elif choice == "10":
                mode = input("1) 加密 2) 解密: ").strip()
                text = input("請輸入內容: ")
                pwd = input("請輸入自訂金鑰/密碼: ")
                res = crypto_engine.chacha20_encrypt(text, pwd) if mode == "1" else crypto_engine.chacha20_decrypt(text, pwd)
                print(f"結果: {res}")
            elif choice == "11":
                text = input("請輸入內容: ")
                print(f"SHA3-256 結果: {crypto_engine.sha3_256_hash(text)}")
            elif choice == "12":
                text = input("請輸入訊息: ")
                sec = input("請輸入金鑰: ")
                print(f"HMAC 結果: {crypto_engine.generate_hmac(text, sec)}")
            elif choice == "13":
                pwd = input("請輸入密碼: ")
                salt = input("請輸入 Salt (預設 default_salt): ") or "default_salt"
                print(f"PBKDF2 結果: {crypto_engine.pbkdf2_hash(pwd, salt)}")
            elif choice == "14":
                text = input("請輸入內容: ")
                print(f"BLAKE2b 結果: {crypto_engine.blake2b_hash(text)}")
            elif choice == "15":
                text = input("請輸入要以 RSA 加密的內容: ")
                cipher, dec = crypto_engine.rsa_demo_encrypt_decrypt(text)
                print(f"RSA 密文: {cipher}\nRSA 解密內容: {dec}")
            elif choice == "16":
                text = input("請輸入要簽名的訊息: ")
                sig, valid = crypto_engine.rsa_demo_sign_verify(text)
                print(f"RSA 簽名: {sig}\n驗章結果: {'成功 (Pass)' if valid else '失敗'}")

        elif choice == "17":
            # 處理翻譯功能
            print("\n" + "-"*40)
            print(" 【選擇目標翻譯語言】")
            print("  [1] 中文 (繁體)    [5] 梵文 (Sanskrit / 天城文)")
            print("  [2] 英文 (English) [6] 日文 (日本語)")
            print("  [3] 丁卡文 (Dinka) [7] 韓文 (한국어)")
            print("  [4] 牙買加方言 (Jamaican Patois)")
            print("-"*40)
            
            lang_choice = input("請選擇目標語言 (1-7): ").strip()
            if lang_choice in TranslationEngine.LANG_MAP:
                src_text = input("請輸入欲翻譯的文字/詞彙: ")
                result = TranslationEngine.translate(src_text, lang_choice)
                print(f"\n【翻譯結果】:\n{result}")
            else:
                print("無效的語言選項。")

        else:
            print("無效選項，請重新輸入。")

if __name__ == "__main__":
    main()
