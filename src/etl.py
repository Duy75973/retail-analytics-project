# src/etl.py
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging

# Thiết lập hệ thống logging để theo dõi tiến trình
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_etl():
    """
    Chạy toàn bộ quy trình ETL:
    1. Extract: Đọc dữ liệu từ file CSV.
    2. Transform: Làm sạch và chuẩn hóa dữ liệu.
    3. Load: Ghi dữ liệu đã xử lý vào database MySQL.
    """
    try:
        # Tải các biến môi trường từ file .env
        load_dotenv()
        logging.info("Đã tải biến môi trường.")

        # Lấy thông tin kết nối database từ biến môi trường
        db_user = os.getenv("MYSQL_USER")
        db_password = os.getenv("MYSQL_PASSWORD")
        db_host = os.getenv("MYSQL_HOST")
        db_port = os.getenv("MYSQL_PORT")
        db_name = os.getenv("MYSQL_DATABASE")

        if not all([db_user, db_password, db_host, db_port, db_name]):
            logging.error("Lỗi: Một hoặc nhiều biến môi trường cho database chưa được thiết lập.")
            return

        # --- EXTRACT ---
        raw_data_path = 'data/raw/online_retail.csv'
        logging.info(f"Bắt đầu bước Extract từ file: {raw_data_path}")
        # Cần chỉ định encoding vì file có thể chứa ký tự đặc biệt
        df = pd.read_csv(raw_data_path, encoding='ISO-8859-1')
        logging.info(f"Đọc thành công {len(df)} dòng dữ liệu thô.")

        # --- TRANSFORM ---
        logging.info("Bắt đầu bước Transform...")
        # Loại bỏ khoảng trắng và chuyển tên cột về chữ thường
        df.columns = df.columns.str.strip().str.lower()
        
        # Chuyển đổi invoice_date sang kiểu datetime
        df['invoicedate'] = pd.to_datetime(df['invoicedate'], format='%m/%d/%Y %H:%M')

        # Xóa các dòng có customerid bị thiếu (vì các phân tích sau này đều dựa trên khách hàng)
        df.dropna(subset=['customerid'], inplace=True)
        
        # Chuyển customerid sang kiểu số nguyên
        df['customerid'] = df['customerid'].astype(int)

        # Loại bỏ các giao dịch trả hàng (có số lượng < 0)
        df = df[df['quantity'] > 0]
        # Loại bỏ các giao dịch có đơn giá bằng 0
        df = df[df['unitprice'] > 0]
        
        logging.info(f"Transform hoàn tất. Dữ liệu còn lại {len(df)} dòng hợp lệ.")

        # --- LOAD ---
        logging.info("Bắt đầu bước Load vào MySQL...")
        connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(connection_string)

        # Ghi DataFrame vào bảng 'transactions'. 
        # if_exists='replace' sẽ xóa bảng cũ và tạo lại. Tốt cho việc chạy lại script từ đầu.
        df.to_sql('transactions', con=engine, if_exists='replace', index=False)
        
        logging.info("Load dữ liệu vào MySQL thành công!")

    except FileNotFoundError:
        logging.error(f"Lỗi: Không tìm thấy file dữ liệu tại '{raw_data_path}'. Hãy chắc chắn bạn đã tải và đặt file vào đúng chỗ.")
    except Exception as e:
        logging.error(f"Đã có lỗi xảy ra trong quá trình ETL: {e}")

if __name__ == "__main__":
    run_etl()