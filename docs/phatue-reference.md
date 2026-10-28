# Tham khảo trình biên tập Phả Tuệ

Đã quan sát trang do người dùng cung cấp trên trình duyệt và đọc HTML cùng bundle JavaScript được website phục vụ công khai. Không có quyền truy cập mã backend hoặc mã Dart nguyên bản.

Trang `https://app.phatue.vn/gia-pha/40j0b6II1FqDjT8aTz5A/ve-pha-do` dùng Flutter Web; giao diện được dựng từ `main.dart.js` đã biên dịch. Các chuỗi giao diện trong bundle xác nhận tùy chỉnh khoảng cách thế hệ, độ dày đường nối, khổ giấy, ảnh/ô dọc, và thiết lập ghi đè theo thế hệ. Phần thực hiện trong dự án này được viết riêng bằng React, React Flow và jsPDF, không nhập mã hoặc tài nguyên trang trí của dịch vụ tham khảo.

Áp dụng vào ứng dụng họ Lại:

- Trình biên tập ba vùng: điều hướng thế hệ, canvas, bảng chỉnh theo phạm vi.
- Mẫu hiện đại và truyền thống bằng CSS nội bộ; tiêu đề và khung bản in.
- Điều chỉnh khoảng cách, màu và độ dày đường nối; thiết lập chung hoặc riêng từng đời.
- Tùy chỉnh ô ngang/dọc, chữ viết tắt, phối ngẫu, cỡ chữ. Không tạo ảnh hoặc năm sinh/mất khi chưa có dữ liệu nguồn.
- Hoàn tác/làm lại tùy chỉnh trong phiên; sắp xếp lại vị trí, mở rộng trình biên tập.
- Lưu trên localStorage theo gốc phả đồ: thiết kế, vị trí các nút đang hiển thị, số thế hệ, trạng thái mở/thu và viewport. Không đồng bộ thiết bị và không sửa quan hệ nguồn.
- Xuất PDF vector với font tiếng Việt nhúng, khổ A0/A1 hoặc tự nhập 200–5000 mm. PDF gồm các nút và liên kết đang hiển thị, kể cả nút ngoài vùng nhìn; giữ dấu hiệu rà soát và dẫn trang nguồn. Tùy chỉnh theo thế hệ được áp dụng vào bản xuất.

Bản PDF đã được tải thử, kiểm tra text Unicode, khổ A0 và dựng ảnh để kiểm tra bố cục.


## Đối chiếu trực quan trình biên tập, 29/10/2026

Đã quan sát đúng `/gia-pha/40j0b6II1FqDjT8aTz5A/ve-pha-do`: cột thế hệ bên trái, công cụ tìm người, danh sách trang trí (hoành phi/rồng chầu/câu đối/nền/khung/ảnh/chữ), canvas ở giữa, bảng phạm vi đời với ô xem trước và thông tin sinh/mất ở bên phải. Bản tham khảo có nút hoàn tác/làm lại, sắp xếp, lưu, xuất PDF và vừa khổ.

Dự án họ Lại bổ sung ô xem trước, ngày sinh/mất, nguồn, ảnh từ album, ba kiểu nối, tìm và đến người, nổi bật trực hệ, khóa kéo, tiêu đề/phụ đề/câu đối và góc khung tự dựng. Đã bổ sung lớp ảnh/chữ tự do, hoành phi và cặp rồng chầu; chưa chuyển toàn bộ mẫu hoa văn hoặc các công cụ chỉnh khung chữ chi tiết của Phả Tuệ. Tài nguyên gốc vẫn được giữ riêng, chỉ tham chiếu các ảnh được chọn làm trang trí. Không truy cập mã máy chủ hoặc tái sử dụng JavaScript ứng dụng Phả Tuệ.

Đã kiểm tra tìm người đời 21, giữ nguyên gốc đời 12 và khoảng trống nguồn; xuất PDF A1 có năm ô, đường cong, ngày húy kỵ và nguồn PDF. Chỉ tọa độ kéo thủ công được bảo lưu qua thay đổi số đời; sửa CSS vào layout gốc để tránh mất bố cục React Flow sau khi tải lại.


## Kiểm tra trang trí mở rộng

Đã quan sát các bảng Hoành phi và Chữ 1 trên trang tham khảo: thay ảnh từ thư viện/tải lên/URL, kích thước ảnh, nội dung chữ, cỡ/màu chữ, khung chữ và căn trái/giữa/phải. Dự án bổ sung tối đa 20 lớp độc lập: hoành phi, rồng chầu, chữ và ảnh. Có kéo/đổi kích thước, chỉnh tọa độ, phông Be Vietnam Pro/Noto Serif, màu/nền/viền, độ đậm, khóa/ẩn, thứ tự, nhân đôi, xóa và hoàn tác. Ảnh lấy từ album hoặc các tài nguyên raster đã tải; không tải URL ảnh ngoài.

Đã kiểm tra bản production riêng: kéo lớp chữ, đổi kích thước 360×100 → 427×133 px, khóa, ẩn, nhân đôi, xóa/hoàn tác/làm lại; lưu và tải lại giữ tọa độ ảnh y=490. PDF chứa hoành phi PNG trong suốt, hai rồng chầu, ảnh từ đường, chữ Việt và nền hình học, không cắt các lớp ngoài vùng cây. Ảnh trang trí từ Phả Tuệ có nguồn trong manifest; không xem là ảnh tổ tiên hoặc thương hiệu họ Lại.
