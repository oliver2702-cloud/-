import base64
import hashlib
import hmac
import urllib.parse
import streamlit as st

# 頁面基本設定
st.set_page_config(page_title="純內建加密與語言轉換系統", layout="wide")


# ----------------------------------------------------------------------
# 加密引擎 (純內建)
# ----------------------------------------------------------------------
class PureCryptoEngine:

  @staticmethod
  def caesar_cipher(text: str, shift: int, decrypt: bool = False) -> str:
    if decrypt:
      shift = -shift
    result = []
    for char in text:
      if char.isalpha():
        start = ord("A") if char.isupper() else ord("a")
        result.append(chr((ord(char) - start + shift) % 26 + start))
      else:
        result.append(char)
    return "".join(result)

  @staticmethod
  def vigenere_cipher(text: str, key: str, decrypt: bool = False) -> str:
    if not key:
      return text
    key = key.upper()
    result = []
    key_idx = 0
    for char in text:
      if char.isalpha():
        shift = ord(key[key_idx % len(key)]) - ord("A")
        if decrypt:
          shift = -shift
        start = ord("A") if char.isupper() else ord("a")
        result.append(chr((ord(char) - start + shift) % 26 + start))
        key_idx += 1
      else:
        result.append(char)
    return "".join(result)

  @staticmethod
  def baconian_encode(text: str) -> str:
    bacon_map = {
        chr(i + 65): f"{i:05b}".replace("0", "A").replace("1", "B")
        for i in range(26)
    }
    return " ".join(
        [bacon_map.get(c.upper(), c) for c in text if c.isalpha()]
    )

  @staticmethod
  def baconian_decode(text: str) -> str:
    reverse_map = {
        f"{i:05b}".replace("0", "A").replace("1", "B"): chr(i + 65)
        for i in range(26)
    }
    tokens = text.upper().split()
    return "".join([reverse_map.get(t, t) for t in tokens])

  @staticmethod
  def atbash_cipher(text: str) -> str:
    result = []
    for char in text:
      if "A" <= char <= "Z":
        result.append(chr(ord("Z") - (ord(char) - ord("A"))))
      elif "a" <= char <= "z":
        result.append(chr(ord("z") - (ord(char) - ord("a"))))
      else:
        result.append(char)
    return "".join(result)

  @staticmethod
  def base32_encode(text: str) -> str:
    return base64.b32encode(text.encode("utf-8")).decode("utf-8")

  @staticmethod
  def base32_decode(text: str) -> str:
    try:
      return base64.b32decode(text.encode("utf-8")).decode("utf-8")
    except Exception as e:
      return f"解碼失敗: {e}"

  @staticmethod
  def base85_encode(text: str) -> str:
    return base64.b85encode(text.encode("utf-8")).decode("utf-8")

  @staticmethod
  def base85_decode(text: str) -> str:
    try:
      return base64.b85decode(text.encode("utf-8")).decode("utf-8")
    except Exception as e:
      return f"解碼失敗: {e}"

  @staticmethod
  def hex_encode(text: str) -> str:
    return text.encode("utf-8").hex()

  @staticmethod
  def hex_decode(text: str) -> str:
    try:
      return bytes.fromhex(text).decode("utf-8")
    except Exception as e:
      return f"解碼失敗: {e}"

  @staticmethod
  def xor_cipher(text: str, key_str: str) -> str:
    if not key_str:
      key_str = "key"
    key_bytes = key_str.encode("utf-8")
    text_bytes = text.encode("utf-8")
    xored = bytes(
        [b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)]
    )
    return base64.b64encode(xored).decode("utf-8")

  @staticmethod
  def xor_decipher(b64_data: str, key_str: str) -> str:
    if not key_str:
      key_str = "key"
    try:
      key_bytes = key_str.encode("utf-8")
      raw_bytes = base64.b64decode(b64_data)
      xored = bytes(
          [b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(raw_bytes)]
      )
      return xored.decode("utf-8")
    except Exception as e:
      return f"解密失敗: {e}"


# ----------------------------------------------------------------------
# 翻譯引擎 (純內建)
# ----------------------------------------------------------------------
class PureTranslationEngine:
  LANGUAGES = {
      "1": "中文 (繁體)",
      "2": "英文 (English)",
      "3": "丁卡文 (Dinka)",
      "4": "牙買加方言 (Jamaican Patois)",
      "5": "梵文 (Sanskrit / 天城文)",
      "6": "日文 (日本語)",
      "7": "韓文 (한국어)",
  }
  DICTIONARY = {
      "你好": {
          "1": "你好",
          "2": "Hello",
          "3": "Möđöng",
          "4": "Whaa gwaan",
          "5": "नमस्ते (Namaste)",
          "6": "こんにちは",
          "7": "안녕하세요",
      },
      "謝謝": {
          "1": "謝謝",
          "2": "Thank you",
          "3": "Yin aca leec",
          "4": "Tanks",
          "5": "धन्यवादः (Dhanyavada)",
          "6": "ありがとう",
          "7": "감사합니다",
      },
      "朋友": {
          "1": "朋友",
          "2": "Friend",
          "3": "Mäth",
          "4": "Bredren",
          "5": "मित्रम् (Mitram)",
          "6": "友達",
          "7": "친구",
      },
      "和平": {
          "1": "和平",
          "2": "Peace",
          "3": "Dör",
          "4": "Irie",
          "5": "शान्तिः (Shanti)",
          "6": "平和",
          "7": "평화",
      },
      "再見": {
          "1": "再見",
          "2": "Goodbye",
          "3": "Coke apath",
          "4": "Lickkle more",
          "5": "पुनर्मिलामः (Punar milamah)",
          "6": "さようなら",
          "7": "안녕히 가세요",
      },
  }

  @classmethod
  def translate(cls, text: str, target_code: str) -> str:
    key = text.strip()
    if key in cls.DICTIONARY and target_code in cls.DICTIONARY[key]:
      return cls.DICTIONARY[key][target_code]
    return f"查無「{text}」的內建對應（支援短語：你好、謝謝、朋友、和平、再見）。"


# ----------------------------------------------------------------------
# Streamlit UI
# ----------------------------------------------------------------------
st.title("🔒 16 項內建加密 & 7 國語言轉換系統")
st.caption("免安裝任何第三方套件 (No `cryptography`, No `deep-translator`)")

tab1, tab2 = st.tabs(["🔐 加密 / 解密 / 雜湊", "🌐 7 國語言轉換"])

with tab1:
  col1, col2 = st.columns([1, 2])
  with col1:
    option = st.selectbox(
        "選擇功能",
        [
            "1. 凱撒密碼",
            "2. 維吉尼亞密碼",
            "3. 培根密碼",
            "4. Atbash 密碼",
            "5. Base32 編/解碼",
            "6. Base85 編/解碼",
            "7. Hex 編/解碼",
            "8. URL 編/解碼",
            "9. XOR 輕量加密",
            "10. ROT13 混淆",
            "11. SHA256 雜湊",
            "12. SHA3-256 雜湊",
            "13. HMAC-SHA256 簽名",
            "14. PBKDF2 密碼加鹽",
            "15. BLAKE2b 雜湊",
            "16. SHA512 雜湊",
        ],
    )
    mode = (
        st.radio("模式", ["加密 / 編碼", "解密 / 解碼"])
        if option.split(".")[0] in ["1", "2", "3", "5", "6", "7", "8", "9"]
        else "計算"
    )

  with col2:
    user_input = st.text_area("輸入文字", "你好，Hello World!", height=100)
    key_input = ""
    shift = 3

    if "維吉尼亞" in option or "XOR" in option or "HMAC" in option:
      key_input = st.text_input("輸入金鑰 / 密碼", "secret_key")
    elif "凱撒" in option:
      shift = st.number_input("位移量", value=3, step=1)
    elif "PBKDF2" in option:
      key_input = st.text_input("Salt (鹽值)", "default_salt")

    if st.button("執行", type="primary"):
      opt_num = option.split(".")[0]
      res = ""
      is_decrypt = mode == "解密 / 解碼"

      if opt_num == "1":
        res = PureCryptoEngine.caesar_cipher(user_input, shift, is_decrypt)
      elif opt_num == "2":
        res = PureCryptoEngine.vigenere_cipher(
            user_input, key_input, is_decrypt
        )
      elif opt_num == "3":
        res = (
            PureCryptoEngine.baconian_encode(user_input)
            if not is_decrypt
            else PureCryptoEngine.baconian_decode(user_input)
        )
      elif opt_num == "4":
        res = PureCryptoEngine.atbash_cipher(user_input)
      elif opt_num == "5":
        res = (
            PureCryptoEngine.base32_encode(user_input)
            if not is_decrypt
            else PureCryptoEngine.base32_decode(user_input)
        )
      elif opt_num == "6":
        res = (
            PureCryptoEngine.base85_encode(user_input)
            if not is_decrypt
            else PureCryptoEngine.base85_decode(user_input)
        )
      elif opt_num == "7":
        res = (
            PureCryptoEngine.hex_encode(user_input)
            if not is_decrypt
            else PureCryptoEngine.hex_decode(user_input)
        )
      elif opt_num == "8":
        res = (
            urllib.parse.quote(user_input)
            if not is_decrypt
            else urllib.parse.unquote(user_input)
        )
      elif opt_num == "9":
        res = (
            PureCryptoEngine.xor_cipher(user_input, key_input)
            if not is_decrypt
            else PureCryptoEngine.xor_decipher(user_input, key_input)
        )
      elif opt_num == "10":
        res = PureCryptoEngine.caesar_cipher(user_input, 13)
      elif opt_num == "11":
        res = hashlib.sha256(user_input.encode()).hexdigest()
      elif opt_num == "12":
        res = hashlib.sha3_256(user_input.encode()).hexdigest()
      elif opt_num == "13":
        res = hmac.new(
            key_input.encode(), user_input.encode(), hashlib.sha256
        ).hexdigest()
      elif opt_num == "14":
        res = hashlib.pbkdf2_hmac(
            "sha256", user_input.encode(), key_input.encode(), 100000
        ).hex()
      elif opt_num == "15":
        res = hashlib.blake2b(user_input.encode()).hexdigest()
      elif opt_num == "16":
        res = hashlib.sha512(user_input.encode()).hexdigest()

      st.success("輸出結果：")
      st.code(res)

with tab2:
  st.subheader("7 國語言詞彙對照")
  target_lang = st.selectbox(
      "選擇目標語言", list(PureTranslationEngine.LANGUAGES.values())
  )
  lang_code = [
      k
      for k, v in PureTranslationEngine.LANGUAGES.items()
      if v == target_lang
  ][0]

  trans_input = st.text_input("輸入詞彙（例如：你好、謝謝、朋友、和平、再見）", "你好")
  if st.button("對照翻譯"):
    out = PureTranslationEngine.translate(trans_input, lang_code)
    st.info(f"**{trans_input}** -> **{out}**")
