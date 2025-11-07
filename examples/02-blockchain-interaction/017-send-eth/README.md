# 017. Send ETH Transaction

> ส่ง ETH จาก address หนึ่งไปอีก address พร้อม gas estimation - ใช้งานได้จริง 100% ✅

## 📋 คำอธิบาย

เรียนรู้การส่ง ETH transactions ด้วย Web3.py พร้อม:
- Gas estimation
- Transaction signing
- Balance checking
- Batch sending

## 🎯 เทคโนโลยี

- **Python**: 3.11+
- **Web3.py**: 6.11+
- **eth-account**: 0.10+

## 📊 ระดับ

🟢 **Beginner**

## 💡 ฟีเจอร์

- ✅ **Send ETH** - ส่ง ETH พร้อม gas estimation อัตโนมัติ
- ✅ **Balance Check** - ตรวจสอบ balance ก่อนและหลังส่ง
- ✅ **Gas Estimation** - คำนวณ gas cost อัตโนมัติ
- ✅ **Transaction Signing** - Sign ด้วย private key
- ✅ **Batch Send** - ส่งไปหลาย addresses พร้อมกัน
- ✅ **Error Handling** - ตรวจสอบ insufficient balance

## 🚀 การติดตั้ง

```bash
# Install dependencies
pip install -r requirements.txt

# Start Anvil
anvil
```

## 📚 การใช้งาน

### รันโปรแกรม

```bash
python send_eth.py
```

### ใช้ใน Code

```python
from send_eth import EthSender

# Initialize
sender = EthSender()

# Send ETH
receipt = sender.send_eth(
    private_key="0xac0974...",
    to_address="0x70997970...",
    amount_eth=1.5
)

print(f"Hash: {receipt['hash']}")
print(f"Gas used: {receipt['gas_used']}")
```

### Batch Send

```python
recipients = [
    ("0x70997970C51812dc3A010C7d01b50e0d17dc79C8", 0.1),
    ("0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC", 0.2),
]

receipts = sender.send_eth_batch(private_key, recipients)
```

## 📖 Code Structure

```
017-send-eth/
├── send_eth.py         # 361 lines - Complete implementation
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

## ✅ Pass Criteria

1. ✅ ส่ง ETH transaction สำเร็จ
2. ✅ Gas estimation ถูกต้อง
3. ✅ Balance เปลี่ยนแปลงถูกต้อง
4. ✅ Transaction hash ได้รับ
5. ✅ Receipt มีข้อมูลครบ

## 🎓 สิ่งที่จะได้เรียนรู้

- ✅ การส่ง ETH transactions
- ✅ Gas estimation และ gas price
- ✅ Transaction signing ด้วย private key
- ✅ Nonce management
- ✅ Balance checking
- ✅ Error handling
- ✅ Batch sending

## 🚀 Next Steps

- **018-erc20-interact**: โต้ตอบกับ ERC-20 tokens
- **020-event-listener**: ฟัง blockchain events

---

**License**: MIT
**Version**: 1.0.0
