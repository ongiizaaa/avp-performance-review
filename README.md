# AVP Performance Review

เว็บแอปคำนวณผลตอบแทนพอร์ตกองทุนลูกค้า (XIRR และผลตอบแทนถ่วงน้ำหนักต้นทุนตามเวลา) จากไฟล์รายการซื้อขายของกรุงศรีและฟิลลิป
แล้วสร้างไฟล์ Excel ตาม template "Performance Review"

- ใช้งาน: https://avp-performance-review.netlify.app (ติดตั้งเป็นแอปได้จาก Chrome หรือ Safari)
- ไฟล์ลูกค้าถูกอ่านในเบราว์เซอร์เท่านั้น ไม่มีการอัปโหลด และแอปไม่เก็บข้อมูลลูกค้า

## โครงสร้าง

| ไฟล์ | หน้าที่ |
|---|---|
| `src/app.html` | ต้นฉบับของแอป (หน้าจอ, สไตล์, สคริปต์) แก้ที่นี่ที่เดียว |
| `src/template-base.xlsx` | template Performance Review ที่ล้าง external link แล้ว แอปเติมข้อมูลลงไฟล์นี้ |
| `src/template-static.json` | ข้อความและ style id คงที่ของ template |
| `tools/build.py` | สร้าง `site/index.html` และ `site/sw.js` จาก `src/` |
| `site/` | ไฟล์ที่ Netlify เผยแพร่ (commit ไว้แล้ว ไม่มีขั้น build บน Netlify) |

## การอัปเดต

1. แก้ `src/app.html`
2. `python3 tools/build.py`
3. commit และ push ไปที่ `main` แล้ว Netlify จะ deploy ให้อัตโนมัติ

## กติกาการคำนวณ (ตรงกับ template เดิม)

- แยกคำนวณตามเลขบัญชี ไม่รวมกรุงศรีกับฟิลลิป
- Buy / Switch In / SWI = ซื้อ, Sell / Switch Out / SWO = ขาย, Dividend = ปันผล
- กรุงศรีใช้ Trade Date, ฟิลลิปใช้ "เวลาส่งคำสั่ง" (เปลี่ยนเป็นวันลงทุนได้ในแอป) และนับเฉพาะสถานะ Order Done
- มูลค่าพอร์ต ณ วันเริ่มต้น = H3, มูลค่าพอร์ต ณ วันสิ้นสุด = แถววันสิ้นสุด คอลัมน์ N
- ตรวจแล้วผลตรงกับไฟล์ template ที่ทำมือทั้งฝั่งกรุงศรีและฟิลลิป
