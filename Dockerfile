# 
# Bước 1: Chọn một image nền. Lấy một image Python 3.9 bản gọn nhẹ.
FROM python:3.9-slim

# Bước 2: Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Bước 3: Sao chép file requirements.txt vào container
COPY requirements.txt .

# Bước 4: Cài đặt các thư viện Python cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Bước 5: Sao chép toàn bộ source code của dự án vào container
COPY . .

# Bước 6: Lệnh mặc định sẽ được chạy khi container khởi động
CMD ["python", "src/etl.py"]