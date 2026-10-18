# بوت البرودكاست (منفصل)

## Railway
1. مشروع جديد من هذا المجلد
2. Variables:
   - `DISCORD_TOKEN` = توكن البوت
   - `BC_ENCRYPT_KEY` = 64 حرف hex (اختياري لتشفير توكنات البرود)
   - Volume على `/data` و `BOT_DATA_DIR=/data`
3. Deploy

## أوامر مهمة
- `/send-broadcast-panel` — لوحة البرود
- `/refresh-broad` — تحديث الأرقام على اللوحة
- باقي الأوامر من اللوحة (توكنات / رسالة / إرسال)

## ملاحظات
- فعّل **Server Members** و **Presence** و **Message Content** من Developer Portal
- هذا البوت مستقل عن البوت الرئيسي
