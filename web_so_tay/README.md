# Sổ tay tinh hoa — trang web đọc offline
- Dựng lại (mỗi khi sổ tay / moc / giá / ảnh thay đổi): `cd trade_dai_han && python3 web_so_tay/build.py` → ghi `web_so_tay/index.html` (+ ảnh thu nhỏ `thumbs/`, tạo bằng `sips`).
- Mở: bấm đúp `web_so_tay/index.html` (hoặc `open web_so_tay/index.html`) — chạy qua file://, không cần mạng, không cần server.
- Thư viện tải sẵn 1 lần trong `vendor/`: markdown 3.7 (Python, `vendor/py`), lightweight-charts 4.2.3, Chart.js 4.4.7; thiếu thì cài lại: `python3 -m pip install --target web_so_tay/vendor/py markdown==3.7`.
- Mọi số liệu/hình tính từ file lúc build; thiếu ghi chú ảnh (`so_tay/ghi_chu/hinh_anh_*.md`) vẫn chạy, ảnh hiện "chưa có ghi chú".
