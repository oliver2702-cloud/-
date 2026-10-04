import base64
import hashlib
import hmac
import os
import urllib.parse

# ----------------------------------------------------------------------
# 1. 完全內建加密/解密/編碼引擎 (16 項功能，無須第三方套件)
# ----------------------------------------------------------------------

class PureCryptoEngine:

    # 1. 凱撒密碼 (Caesar Cipher)
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

    # 2. 維吉尼亞密碼 (Vigenère Cipher)
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

    # 3. 培根密碼 (Baconian Cipher)
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
            res.append(reverse_map.get(token, token))
        return "".join(res)

    # 4. Atbash 密碼 (阿特巴什密碼)
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

    # 5. Base32 編碼 / 解碼
    @staticmethod
    def base32_encode(text: str) -> str:
        return base64.b32encode(text.encode('utf-8')).decode('utf-8')

    @staticmethod
    def base32_decode(encoded_str: str) -> str:
        return base64.b32decode(encoded_str.encode('utf-8')).decode('utf-8')

    # 6. Base85 編碼 / 解碼
    @staticmethod
    def base85_encode(text: str) -> str:
        return base64.b85encode(text.encode('utf-8')).decode('utf-8')

    @staticmethod
    def base85_decode(encoded_str: str) -> str:
        return base64.b85decode(encoded_str.encode('utf-8')).decode('utf-8')

    # 7. Hex (十六進位) 編碼 / 解碼
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

    # 9. XOR 輕量流加密 (替代需要外部庫的 AES)
    @staticmethod
    def xor_cipher(text: str, key_str: str) -> str:
        if not key_str:
            key_str = "key"
        key_bytes = key_str.encode('utf-8')
        text_bytes = text.encode('utf-8')
        xored = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])
        return base64.b64encode(xored).decode('utf-8')

    @staticmethod
    def xor_decipher(b64_data: str, key_str: str) -> str:
        if not key_str:
            key_str = "key"
        key_bytes = key_str.encode('utf-8')
        raw_bytes = base64.b64decode(b64_data)
        xored = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(raw_bytes)])
        return xored.decode('utf-8')

    # 10. ROT13 經典文字混淆
    @staticmethod
    def rot13(text: str) -> str:
        return PureCryptoEngine.caesar_cipher(text, 13)

    # 11. SHA256 雜湊
    @staticmethod
    def sha256_hash(text: str) -> str:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    # 12. SHA3-256 雜湊
    @staticmethod
    def sha3_256_hash(text: str) -> str:
        return hashlib.sha3_256(text.encode('utf-8')).hexdigest()

    # 13. HMAC-SHA256 簽名生成
    @staticmethod
    def generate_hmac(message: str, secret_key: str) -> str:
        return hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

    # 14. PBKDF2 密碼安全雜湊 (內建加鹽機制)
    @staticmethod
    def pbkdf2_hash(password: str, salt_str: str = "default_salt") -> str:
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt_str.encode('utf-8'),
            100000
        )
        return key.hex()

    # 15. BLAKE2b 雜湊
    @staticmethod
    def blake2b_hash(text: str) -> str:
        return hashlib.blake2b(text.encode('utf-8')).hexdigest()

    # 16. SHA512 高強度雜湊
    @staticmethod
    def sha512_hash(text: str) -> str:
        return hashlib.sha512(text.encode('utf-8')).hexdigest()


# ----------------------------------------------------------------------
# 2. 完全內建多語言對照引擎 (含 7 國語言/方言/梵文)
# ----------------------------------------------------------------------

class PureTranslationEngine:
    """純 Python 內建語言對照模組 (不需連線與下載外部套件)"""

    LANGUAGES = {
        "1": "中文 (繁體)",
        "2": "英文 (English)",
        "3": "丁卡文 (Dinka)",
        "4": "牙買加方言 (Jamaican Patois)",
        "5": "梵文 (Sanskrit / 天城文)",
        "6": "日文 (日本語)",
        "7": "韓文 (한국어)"
    }

    # 內建多國語言常用對照表
    DICTIONARY = {
        "你好": {
            "1": "你好", "2": "Hello", "3": "Möđöng", 
            "4": "Whaa gwaan", "5": "नमस्ते (Namaste)", "6": "こんにちは", "7": "안녕하세요"
        },
        "謝謝": {
            "1": "謝謝", "2": "Thank you", "3": "Yin aca leec", 
            "4": "Tanks", "5": "धन्यवादः (Dhanyavada)", "6": "ありがとう", "7": "감사합니다"
        },
        "朋友": {
            "1": "朋友", "2": "Friend", "3": "Mäth", 
            "4": "Bredren", "5": "मित्रम् (Mitram)", "6": "友達", "7": "친구"
        },
        "和平": {
            "1": "和平", "2": "Peace", "3": "Dör", 
            "4": "Irie", "5": "शान्तिः (Shanti)", "6": "平和", "7": "평화"
        },
        "再見": {
            "1": "再見", "2": "Goodbye", "3": "Coke apath", 
            "4": "Lickkle more", "5": "पुनर्मिलामः (Punar milamah)", "6": "さようなら", "7": "안녕히 가세요"
        }
    }

    @classmethod
    def translate(cls, text: str, target_code: str) -> str:
        key = text.strip()
        if key in cls.DICTIONARY and target_code in cls.DICTIONARY[key]:
            return cls.DICTIONARY[key][target_code]
        
        target_name = cls.LANGUAGES.get(target_code, "未知的語言")
        return f"[詞庫無精確對應]: 查無「{text}」在 {target_name} 中的內建詞條（目前支援對照短語：你好、謝謝、朋友、和平、再見）。"


# ----------------------------------------------------------------------
# 3. 命令列主介面 (CLI)
# ----------------------------------------------------------------------

def main():
    engine = PureCryptoEngine()
    
    while True:
        print("\n" + "="*50)
        print("   16 項內建模組加密解密 & 7 國語言轉換系統   ")
        print("="*50)
        print(" 【純內建加密與解密】")
        print("  [1]  凱撒密碼          [9]  XOR 輕量加密/解密")
        print("  [2]  維吉尼亞密碼      [10] ROT13 文字混淆")
        print("  [3]  培根密碼          [11] SHA256 雜湊")
        print("  [4]  Atbash 密碼       [12] SHA3-256 雜湊")
        print("  [5]  Base32 編解碼     [13] HMAC-SHA256 簽名")
        print("  [6]  Base85 編解碼     [14] PBKDF2 密碼加鹽雜湊")
        print("  [7]  Hex 編解碼        [15] BLAKE2b 雜湊")
        print("  [8]  URL 編解碼        [16] SHA512 雜湊")
        print("--------------------------------------------------")
        print(" 【純內建多語言轉換】")
        print("  [17] 進入 7 國語言翻譯器 (中/英/丁卡/牙買加/梵/日/韓)")
        print("--------------------------------------------------")
        print("  [0]  退出系統")
        print("="*50)
        
        choice = input("請選擇功能項目 (0-17): ").strip()
        
        if choice == "0":
            print("\n系統已退出。")
            break
            
        elif choice in [str(i) for i in range(1, 17)]:
            if choice == "1":
                mode = input("1) 加密 2) 解密: ").strip()
                text = input("請輸入內容: ")
                shift = int(input("位移量 (預設3): ") or 3)
                print(f"結果: {engine.caesar_cipher(text, shift, decrypt=(mode == '2'))}")
            elif choice == "2":
                mode = input("1) 加密 2) 解密: ").strip()
                text = input("請輸入內容: ")
                key = input("請輸入金鑰: ")
                print(f"結果: {engine.vigenere_cipher(text, key, decrypt=(mode == '2'))}")
            elif choice == "3":
                mode = input("1) 編碼 2) 解碼: ").strip()
                text = input("請輸入內容: ")
                print(f"結果: {engine.baconian_encode(text) if mode == '1' else engine.baconian_decode(text)}")
            elif choice == "4":
                text = input("請輸入內容: ")
                print(f"結果: {engine.atbash_cipher(text)}")
            elif choice == "5":
                mode = input("1) 編碼 2) 解碼: ").strip()
                text = input("請輸入內容: ")
                print(f"結果: {engine.base32_encode(text) if mode == '1' else engine.base32_decode(text)}")
            elif choice == "6":
                mode = input("1) 編碼 2) 解碼: ").strip()
                text = input("請輸入內容: ")
                print(f"結果: {engine.base85_encode(text) if mode == '1' else engine.base85_decode(text)}")
            elif choice == "7":
                mode = input("1) 編碼 2) 解碼: ").strip()
                text = input("請輸入內容: ")
                print(f"結果: {engine.hex_encode(text) if mode == '1' else engine.hex_decode(text)}")
            elif choice == "8":
                mode = input("1) 編碼 2) 解碼: ").strip()
                text = input("請輸入內容: ")
                print(f"結果: {engine.url_encode(text) if mode == '1' else engine.url_decode(text)}")
            elif choice == "9":
                mode = input("1) 加密 2) 解密: ").strip()
                text = input("請輸入內容: ")
                pwd = input("請輸入金鑰/密碼: ")
                print(f"結果: {engine.xor_cipher(text, pwd) if mode == '1' else engine.xor_decipher(text, pwd)}")
            elif choice == "10":
                text = input("請輸入內容: ")
                print(f"結果: {engine.rot13(text)}")
            elif choice == "11":
                text = input("請輸入內容: ")
                print(f"SHA256 結果: {engine.sha256_hash(text)}")
            elif choice == "12":
                text = input("請輸入內容: ")
                print(f"SHA3-256 結果: {engine.sha3_256_hash(text)}")
            elif choice == "13":
                text = input("請輸入訊息: ")
                sec = input("請輸入金鑰: ")
                print(f"HMAC 結果: {engine.generate_hmac(text, sec)}")
            elif choice == "14":
                pwd = input("請輸入密碼: ")
                salt = input("請輸入 Salt (預設 default_salt): ") or "default_salt"
                print(f"PBKDF2 結果: {engine.pbkdf2_hash(pwd, salt)}")
            elif choice == "15":
                text = input("請輸入內容: ")
                print(f"BLAKE2b 結果: {engine.blake2b_hash(text)}")
            elif choice == "16":
                text = input("請輸入內容: ")
                print(f"SHA512 結果: {engine.sha512_hash(text)}")

        elif choice == "17":
            print("\n" + "-"*40)
            print(" 【選擇目標翻譯語言】")
            print("  [1] 中文 (繁體)    [5] 梵文 (Sanskrit / 天城文)")
            print("  [2] 英文 (English) [6] 日文 (日本語)")
            print("  [3] 丁卡文 (Dinka) [7] 韓文 (한국어)")
            print("  [4] 牙買加方言 (Jamaican Patois)")
            print("-"*40)
            
            lang_choice = input("請選擇目標語言 (1-7): ").strip()
            if lang_choice in PureTranslationEngine.LANGUAGES:
                src_text = input("請輸入欲翻譯詞彙 (試試看: 你好、謝謝、朋友、和平、再見): ")
                result = PureTranslationEngine.translate(src_text, lang_choice)
                print(f"\n【對照結果】:\n{result}")
            else:
                print("無效的語言選項。")

        else:
            print("無效選項，請重新輸入。")

if __name__ == "__main__":
    main()
