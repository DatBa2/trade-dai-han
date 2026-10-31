#!/bin/bash
# In ra (KHÔNG tự cài) dòng crontab chạy lệnh giấy 5 phút sau mỗi nến H4 đóng.
# Nến H4 OKX đóng lúc 00/04/08/12/16/20 giờ UTC = 07/11/15/19/23/03 giờ VN
# → chạy lúc 03:05, 07:05, 11:05, 15:05, 19:05, 23:05 giờ VN.
# Máy ngủ / tắt làm lỡ lịch thì không sao: lần chạy sau tự xử lý bù mọi nến bị lỡ (chay_giay.py idempotent).
set -e
THU_MUC="$(cd "$(dirname "$0")/.." && pwd)"
PY="$(command -v python3)"
GIO="$("$PY" -c '
import time
lech = -time.timezone if not time.localtime().tm_isdst else -time.altzone   # giây lệch so với UTC của máy
print(",".join(str(h) for h in sorted(((h_vn - 7) * 3600 + lech) // 3600 % 24 for h_vn in (3, 7, 11, 15, 19, 23))))
')"
DONG="5 $GIO * * * cd $THU_MUC && $PY giay/chay_giay.py >> giay/cron.log 2>&1"
echo "# Múi giờ máy: $(date +%Z) ($(date +%z)) → giờ chạy theo đồng hồ máy: $GIO (phút 05)"
echo "$DONG"
echo
echo "# Để cài (tự làm, script này không cài):"
echo "#   (crontab -l 2>/dev/null; echo '$DONG') | crontab -"
echo "# Kiểm: crontab -l   ·   Gỡ: crontab -l | grep -v chay_giay.py | crontab -"
