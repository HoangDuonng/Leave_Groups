# Telegram Leave Groups

Script Python giúp xem các group trong một Telegram folder và chọn group muốn out.

## 1. Chuẩn bị

- Cài Python 3.
- Cài thư viện Telethon:

```bash
pip install telethon
```

- Lấy `api_id` và `api_hash` tại: https://my.telegram.org/apps

## 2. Điền thông tin vào `leave_groups.py`

Mở file `leave_groups.py` và sửa các dòng cấu hình ở đầu file:

```python
api_id = YOUR_API_ID_HERE
api_hash = "YOUR_API_HASH_HERE"
FOLDER_NAME = "YOUR_TELEGRAM_FOLDER_NAME_HERE"
client = TelegramClient("YOUR_SESSION_NAME_HERE", api_id, api_hash)
```

Ví dụ:

```python
api_id = 123456
api_hash = "abcdef123456abcdef123456abcdef12"
FOLDER_NAME = "Work"
client = TelegramClient("my_telegram_session", api_id, api_hash)
```

Lưu ý: `api_id` là số nên không dùng dấu `""`; các giá trị còn lại là chữ nên giữ dấu `""`.

## 3. Chạy script

```bash
python3 leave_groups.py
```

Lần đầu chạy, Telegram sẽ yêu cầu nhập số điện thoại, mã OTP và có thể cả mật khẩu 2FA.

Sau đó script sẽ hiện danh sách group trong folder đã chọn. Tick group muốn out rồi bấm **OUT SELECTED**. Nếu máy không hỗ trợ giao diện, nhập số group trong terminal, ví dụ `1,3,5` hoặc `2-4`.

## 4. Không push file session lên Git

Sau khi đăng nhập, Telethon sẽ tạo file `.session`. File này chứa thông tin đăng nhập, không để lộ file này.

Nên thêm vào `.gitignore`:

```gitignore
*.session
*.session-journal
__pycache__/
*.pyc
```
