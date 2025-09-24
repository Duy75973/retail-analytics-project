-- sql/schema.sql
-- Chọn database để làm việc
USE retail_db;

-- Xóa bảng nếu nó đã tồn tại để tránh lỗi khi chạy lại
DROP TABLE IF EXISTS transactions;

-- Tạo bảng transactions để lưu trữ dữ liệu bán lẻ
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,          -- Khóa chính tự tăng để định danh mỗi dòng
    InvoiceNo VARCHAR(20),                      -- Mã hóa đơn (kiểu chuỗi vì có thể chứa chữ)
    StockCode VARCHAR(20),                      -- Mã sản phẩm
    Description VARCHAR(255),                   -- Mô tả sản phẩm
    Quantity INT,                               -- Số lượng
    InvoiceDate DATETIME,                       -- Ngày giờ xuất hóa đơn
    UnitPrice DECIMAL(10, 2),                   -- Đơn giá (DECIMAL để chính xác về tài chính)
    CustomerID INT,                             -- ID Khách hàng
    Country VARCHAR(50)                         -- Quốc gia
);