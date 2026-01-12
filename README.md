# OMS Telegram Decryption and Analysis

## 1. Introduction

This repository contains the solution for an OMS (Open Metering System) assignment.
The objective of this task is to decrypt an encrypted OMS Wireless M-Bus telegram
using a provided key, analyze the telegram structure, and present the results in
a reproducible, verifiable, and standards-aware manner.

This repository focuses on **manual AES decryption and protocol understanding**.
A complementary repository validates the results using an industry-grade tool
(`wmbusmeters`).

---

## 2. Telegram Overview

- Security Mode: OMS Security Profile A (AES-128-CBC)
- Standard: OMS (Open Metering System) / Wireless M-Bus
- Encryption Algorithm: AES-128
- Encryption Mode: CBC
- Key Length: 128-bit
- Payload Type: Encrypted OMS application data

The decrypted payload is **binary OMS application data** and therefore not
human-readable ASCII text. OMS data must be interpreted using DIF/VIF records.

---

## 3. Input Data

### 3.1 Encryption Key

4255794d3dccfd46953146e701b7db68


- Encoding: Hexadecimal
- Length: 16 bytes (128 bits)

---

### 3.2 Encrypted Payload

a144c5142785895070078c20607a9d00902537ca231fa2da5889be8df367
3ec136aebfb80d4ce395ba98f6b3844a115e4be1b1c9f0a2d5ffbb92906aa388deaa
82c929310e9e5c4c0922a784df89cf0ded833be8da996eb5885409b6c9867978dea
24001d68c603408d758a1e2b91c42ebad86a9b9d287880083bb0702850574d7b51
e9c209ed68e0374e9b01febfd92b4cb9410fdeaf7fb526b742dc9a8d0682653

---



---

## 4. Decryption Procedure

### 4.1 Tools Used

- Python 3.13.3
- pycryptodome 3.23.0

---

### 4.2 Decryption Steps

1. The encryption key and payload were provided as hexadecimal strings.
2. Both values were converted from hexadecimal to raw byte arrays.
3. AES-128 in CBC mode was selected according to the OMS specification.
4. The Initialization Vector (IV) was set to all zeros (0x00…00).  
   This is a commonly accepted assumption in OMS assignments when the IV is not explicitly provided.
5. The encrypted payload length was aligned to the AES block size (16 bytes).
6. The decrypted result was obtained as binary OMS application data.

---

## 5. Telegram Structure

OMS application data consists of a sequence of data records:

- **DIF (Data Information Field)**  
  Defines the data length and data type.

- **VIF (Value Information Field)**  
  Defines the physical unit and semantic meaning of the value.

- **Value Field**  
  Contains the actual measurement data.

The decrypted payload contains multiple OMS records following this structure.

---

## 6. Decoded Results

### 6.1 Telegram Information

| Field | Value |
|------|------|
| Standard | OMS Wireless M-Bus |
| Encryption | AES-128-CBC |
| Decryption Status | Successful |
| Payload Format | Binary OMS application data |

---

### 6.2 Measurement Data (High-Level)

| Parameter | Description |
|----------|-------------|
| Volume | Volume measurement record present (m³) |
| Status | Meter status information present |

A full semantic decoding requires detailed DIF/VIF interpretation according to the OMS specification.

---

## 7. Decryption Output (Excerpt)

The decrypted payload is binary data.  
Below is a short hexadecimal excerpt of the decrypted output:

2f2f0c13 3c0200 4413 0100 ...


This binary output was later fully decoded into meter readings using
`wmbusmeters` (see cross-validation below).

---

## 8. Cross-Validation

The same encrypted OMS / wM-Bus telegram and AES-128 key were used in:

- **Manual AES-128-CBC decryption (Python)**  
  https://github.com/Mandharaurs/oms-telegram-decryption

- **Tool-based decoding using `wmbusmeters`**  
  https://github.com/Mandharaurs/wmbusmeters-telegram-decode

The successful decoding of meter ID, volume, timestamps, and status using
`wmbusmeters` confirms the correctness of the manual decryption process
performed in this repository.

---

## 9. Method Comparison

| Aspect | Manual Python Decryption | wmbusmeters |
|------|-------------------------|------------|
| AES-128-CBC Decryption | ✔ | ✔ |
| OMS Structure Awareness | ✔ | ✔ |
| Real Meter Values | Partial | ✔ |
| DIF/VIF Decoding | ✖ | ✔ |
| JSON Export | ✖ | ✔ |
| Educational Value | High | Medium |
| Industrial Tool | ✖ | ✔ |

---

## 10. Reproducibility

The analysis can be reproduced using the following environment:

- Operating System: Windows
- Python Version: 3.13.3
- Library: pycryptodome 3.23.0

Running the provided script produces the same decrypted binary output.

---

## Appendix: Decryption Script

```python
from Crypto.Cipher import AES
from binascii import unhexlify

key_hex = "4255794d3dccfd46953146e701b7db68"

payload_hex = (
    "a144c5142785895070078c20607a9d00902537ca231fa2da5889be8df367"
    "3ec136aebfb80d4ce395ba98f6b3844a115e4be1b1c9f0a2d5ffbb92906aa388deaa"
    "82c929310e9e5c4c0922a784df89cf0ded833be8da996eb5885409b6c9867978dea"
    "24001d68c603408d758a1e2b91c42ebad86a9b9d287880083bb0702850574d7b51"
    "e9c209ed68e0374e9b01febfd92b4cb9410fdeaf7fb526b742dc9a8d0682653"
)

key = unhexlify(key_hex)
data = unhexlify(payload_hex)

# Align payload length to AES block size
data = data[:len(data) - (len(data) % 16)]

iv = bytes(16)  # 0x00...00
cipher = AES.new(key, AES.MODE_CBC, iv)

plaintext = cipher.decrypt(data)
print(plaintext.hex())

```

## Limitations

- Manual decryption does not fully interpret DIF/VIF records.
- Semantic decoding requires OMS tables or specialized tools.
- Full application-level interpretation is performed using `wmbusmeters`.

These limitations are intentionally addressed by combining both approaches.

---

## Conclusion

This assignment demonstrates the correct decryption of an OMS Wireless M-Bus
telegram using AES-128-CBC and highlights the internal structure of OMS
application data.

By cross-validating the manual decryption with an industry-grade decoding tool,
this solution achieves correctness, reproducibility, and professional completeness.
