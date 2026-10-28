# Đối chiếu Phả Tuệ và dự án gia phả họ Lại

Nguồn: [Phả Tuệ](https://app.phatue.vn/gia-pha/). Khảo sát giao diện demo và mã JavaScript công khai được biên dịch từ Flutter Web. Không có mã Dart gốc hoặc mã máy chủ.

## Trang gia phả

| Tuyến nguồn | Mục tương ứng | Bằng chứng |
|---|---|---|
| `/gia-pha` | home | Đã quan sát trạng thái demo; xem chi tiết JSON |
| `/gia-pha/:id` | home | Đã quan sát trạng thái demo; xem chi tiết JSON |
| `/gia-pha/:id/chinh-sua-voi-cay-gia-pha` | tree,people | Đã quan sát trạng thái demo; xem chi tiết JSON |
| `/gia-pha/:id/danh-ba` | contacts | Có trong bộ định tuyến công khai; trang riêng chưa xác minh trực quan |
| `/gia-pha/:id/danh-sach-nhanh` | branches | Có trong bộ định tuyến công khai; trang riêng chưa xác minh trực quan |
| `/gia-pha/:id/danh-sach-thanh-vien` | people | Có trong bộ định tuyến công khai; trang riêng chưa xác minh trực quan |
| `/gia-pha/:id/giao-dien` | tree | Có trong bộ định tuyến công khai; trang riêng chưa xác minh trực quan |
| `/gia-pha/:id/ho-so` | stories | Có trong bộ định tuyến công khai; trang riêng chưa xác minh trực quan |
| `/gia-pha/:id/tai-san` | assets,finance | Có trong bộ định tuyến công khai; trang riêng chưa xác minh trực quan |
| `/gia-pha/:id/trang-chu` | people | Đã quan sát trạng thái demo; xem chi tiết JSON |
| `/gia-pha/:id/tu-duong` | altar | Có trong bộ định tuyến công khai; trang riêng chưa xác minh trực quan |
| `/gia-pha/:id/ve-pha-do` | tree | Đã quan sát trạng thái demo; xem chi tiết JSON |

Một số đường dẫn chi tiết trả về trang trung tâm trong phiên demo hiện tại; chưa xác định chắc nguyên nhân. Có ghi chép chi tiết trong `phatue-feature-audit.json`. Không coi tên tuyến là bằng chứng đã kiểm tra hết hành vi trang.

## Đã triển khai độc lập

- Phả đồ canvas và trình thiết kế theo thế hệ, lưu bố cục trình duyệt, xuất PDF vector.
- Hồ sơ thành viên thêm/sửa, cha/mẹ, phối ngẫu, tiểu sử, liên hệ, liên kết ảnh; kiểm tra vòng lặp quan hệ, lưu trữ/khôi phục.
- Danh sách chi/cành, danh bạ, tìm đường quan hệ dựa trên ID thực tế.
- Phả ký và sách PDF A4 có mục lục; album ảnh tải lên, phân album và gắn thành viên.
- Lịch âm dương GMT+7, Can Chi, ngày húy kỵ, sự kiện âm/dương và xuất ICS ngày dương.
- Từ đường, bài tưởng niệm, trò chơi kiến thức từ quan hệ có nguồn.
- Quỹ thu chi và vận động, tài sản; số dư và tiến độ lấy từ giao dịch thực tế.
- Duyệt đóng góp, nhật ký thay đổi, cài đặt, lưu trữ và khôi phục, sao lưu JSON, Excel 14 trang tính.

Dữ liệu nền 1.231 hồ sơ và 1.215 quan hệ có nguồn vẫn được giữ riêng. Các liên kết cần rà soát không được tự coi là chắc chắn, khoảng trống đời 11–12 chưa bị nối giả.

## Tài nguyên tải về

Manifest tại `reference/phatue/asset-manifest.json`: tải thành công 85/86 tài nguyên, gồm 74 ảnh và 11 phông chữ. Có URL nguồn, loại tệp, dung lượng và SHA-256. Một tài nguyên không tải được. Các ảnh được xem trong thư viện tham khảo tại Cài đặt & dữ liệu. Giấy phép tái phân phối chưa được xác lập; chưa dùng logo, ảnh đại diện hoặc hình thờ mẫu làm dữ liệu thật của họ Lại. JavaScript ứng dụng nguồn chỉ nằm trong thư mục tạm phục vụ nghiên cứu, không tích hợp vào runtime.

## Phạm vi chưa chuyển sang

Tài khoản/phân quyền nhiều người, chia sẻ trực tuyến, dịch vụ AI, thanh toán, tiền ảo, cửa hàng và mạng xã hội là dịch vụ riêng của nền tảng. Dự án hiện là một không gian dòng họ chạy nội bộ bằng Node và JSON, chưa có các dịch vụ đó. Không sử dụng khóa API hoặc máy chủ Phả Tuệ để giả lập chức năng.

Lịch dùng [Lịch Ta](https://github.com/zeforc/lichta), múi giờ GMT+7, phạm vi 1800–2199. Chỉ quy đổi lịch và Can Chi; không suy diễn ngày tốt/xấu. Ngày giỗ tháng nhuận cần gia đình xác nhận.
