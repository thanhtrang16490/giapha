# Lại tộc · Gia phả chi Diêm Điền

Webapp Next.js, React, TypeScript; giao diện tiếng Việt, thích ứng điện thoại và máy tính. Dữ liệu JSON đặt trong `data_json/`.

## Chạy ứng dụng

```bash
npm install
npm run dev
```

Chế độ phát triển dùng Webpack để tránh lỗi chunk động của Turbopack trong phiên bản Next.js đang cài; bản production vẫn build bình thường.

Mở http://localhost:3000. Phả đồ canvas có đường dẫn http://localhost:3000/#tree.

```bash
npm run typecheck
npm test
npm run build
npm start
```

## Chức năng

- Tổng quan chi họ với ảnh từ đường trích từ tài liệu gốc.
- Canvas React Flow: kéo nền, cuộn để dịch chuyển, chụm hai ngón/Ctrl + cuộn để thu phóng; kéo nút để sắp xếp tạm, căn toàn cây, toàn màn hình, bản đồ thu nhỏ. Có lựa chọn gốc nhánh, toàn bộ hồ sơ, và sơ đồ thế hệ truyền thống. Thay đổi bố cục không sửa quan hệ huyết thống.
- Canvas mặc định hiển thị 3 thế hệ. Chọn 2/3/4/tất cả hoặc mở rộng từng nút người con; có tìm người làm gốc, rà soát hồ sơ và xem nguồn của từng liên kết. Chỉ dựng các nút trong vùng nhìn để giữ thao tác mượt với cây lớn.
- Danh bạ tìm tên và dị bản không dấu, lọc thế hệ/cành/loại dữ liệu, phân trang. Mặc định chỉ hiển thị hồ sơ phả đồ; dữ liệu trích xuất thô nằm ở bộ lọc riêng. Lưu hồ sơ yêu thích trên trình duyệt.
- Hồ sơ cá nhân có quan hệ đã đối chiếu, ghi chú dị bản và trang tài liệu nguồn.
- Giữ ký hiệu DN (con nuôi) trên hồ sơ và đường nối khi ký hiệu nằm cùng dòng tên trong bảng; các ký hiệu chỉ xuất hiện trên sơ đồ ảnh vẫn cần đối chiếu trực quan.
- Lịch âm dương Việt Nam GMT+7 (1800–2199), Can Chi, đánh dấu ngày húy kỵ và sự kiện; tháng nhuận cần gia đình xác định ngày tổ chức.
- Đọc PDF gốc, mở theo số trang PDF, tải tài liệu.
- Biểu mẫu đóng góp lưu bền vững phía máy chủ vào JSON ở trạng thái `pending`. Chưa tự sửa thông tin chính thức.

## Trình biên tập phả đồ

Tham khảo cách tổ chức công cụ của Phả Tuệ; xem ghi chép trong `docs/phatue-reference.md`.

Mở **Phả đồ → Canvas tự do**, rồi nhấn **Mở rộng trình biên tập** ở thanh công cụ. Cột trái chọn đời hoặc mẫu hiện đại/truyền thống. Cột phải chỉnh theo phạm vi đang chọn: khoảng cách, màu/độ dày đường nối, cỡ chữ, ô ngang/dọc, chữ viết tắt và phối ngẫu. Có hoàn tác/làm lại tùy chỉnh trong phiên.

**Lưu bố cục** lưu thiết kế, các vị trí đang hiển thị, trạng thái mở nhánh và góc nhìn trên trình duyệt, riêng từng gốc phả đồ. Chưa đồng bộ thiết bị. **Xuất PDF** tạo bản vector có font tiếng Việt nhúng, chọn khổ A0/A1 hoặc nhập 200–5000 mm. PDF xuất các thế hệ đang hiển thị, gồm cả nút nằm ngoài vùng nhìn. Chọn “Tất cả thế hệ” nếu muốn xuất toàn nhánh. Liên kết cần rà soát luôn giữ nét đứt vàng; chỉnh trình bày không đổi dữ liệu gia phả.

## Dữ liệu và mức độ đối chiếu

Nguồn: `tai_lieu/GIA PHA HO LAI 200325.pdf`, 171 trang PDF; số trang PDF có thể khác số trang in.

- `people-curated.json`: 34 hồ sơ nền từ phả đồ phần chung, giữ riêng làm đầu vào tái tạo.
- `people.json`: 1.231 hồ sơ, 1.215 liên kết cha/mẹ–con có nguồn từ phần chung và 370 hộ thuộc bảy cành. Trong đó 97 liên kết/đời có dị bản hoặc cần đối chiếu và được hiển thị nét đứt. Còn 14 chủ hộ chưa ghép được với dòng con ở hộ cha; giữ riêng, không tự nối. Hai gốc còn lại là Thủy tổ và Lại Thế Năn; khoảng trống đời 11 → 12 vẫn giữ nguyên. Đây là hồ sơ số hóa, chưa khẳng định đã loại bỏ mọi trường hợp trùng người trong tài liệu.
- `households.json`: các ô bảng phục hồi từ tọa độ PDF, giữ mã hộ, mã hộ cha, tên, số đời, số trang và các dòng con.
- `review-issues.json`: 111 mục rà soát (52 dị bản, 45 trường hợp đời cần đối chiếu, 14 chưa nối hộ cha). Mỗi mục có hồ sơ và trang nguồn.
- `records.json`: 1.441 dòng trích xuất từ các bảng. Giữ dòng nguồn, số trang, cành, tên và đời. Chưa gộp người trùng tên; một người có thể có nhiều dòng. Không xem số dòng là số người. Phối ngẫu, năm sinh và mã hộ ở phần sau dòng chưa được tự động gán vì dễ nhầm cột.
- `pages.json`: văn bản trích xuất của toàn bộ 171 trang; sơ đồ dạng ảnh không có đủ nội dung trong văn bản này, cần xem PDF.
- `contributions.json`: các đóng góp chờ rà soát. Lưu tuần tự, ghi tệp tạm rồi đổi tên trong một tiến trình Node. Không hỗ trợ nhiều máy chủ ghi đồng thời.

Để tái tạo dữ liệu trích xuất, cần Poppler (`pdftotext`):

```bash
mkdir -p tmp/pdfs
pdftotext -layout 'tai_lieu/GIA PHA HO LAI 200325.pdf' tmp/pdfs/source.txt
pdftotext -bbox-layout 'tai_lieu/GIA PHA HO LAI 200325.pdf' tmp/pdfs/bbox.html
python3 scripts/extract-data.py
python3 scripts/link-households.py
```

Script giữ nguyên tệp đóng góp đã tồn tại. Khi thay đổi dữ liệu JSON chính thức, build lại bản production. Hai script tái tạo sẽ ghi đè hồ sơ sinh tự động; lưu các chỉnh sửa đã duyệt vào nguồn hoặc quy tắc đối chiếu trước khi tái tạo. Script nối hộ dùng đối chiếu mã hộ hai chiều hoặc tên chính xác trong cùng hộ cha; không dùng so khớp tên gần đúng. Chín trường hợp khác tên ở cành 4 được đối chiếu trực quan các mũi tên ở PDF 90–94 và lưu quy tắc rõ ràng. Giữ nguyên cả tên ghi tại hộ riêng và tên ở danh sách con trong bằng chứng nguồn.

## Phạm vi vận hành

Bản này chạy nội bộ bằng một tiến trình Node, dùng hệ thống tệp có quyền ghi. Có màn hình duyệt đóng góp và nhật ký; chưa có tài khoản, phân quyền; nhãn “Lưu hành nội bộ” mô tả mục đích tài liệu, không phải cơ chế xác thực. Chưa xuất bản lên internet. Nếu triển khai cho nhiều gia đình truy cập từ xa, cần bổ sung xác thực/phân quyền và kho dữ liệu bền vững. Sao lưu `data_json/` cùng tài liệu gốc trước khi cập nhật.

Font Be Vietnam Pro và Noto Serif được phục vụ cục bộ; ảnh từ đường lấy từ trang PDF 14. Không dùng ảnh minh họa giả cho người thật.

## Tham khảo sản phẩm

- FamilySearch — các góc nhìn phả đồ: https://www.familysearch.org/en/help/helpcenter/article/what-are-the-different-pedigree-views-in-family-tree
- MyHeritage — không gian gia đình, hồ sơ, tài liệu và sự kiện: https://www.myheritage.com/help/en/articles/12852603-what-s-the-difference-between-the-family-site-and-family-tree-builder
- React Flow — canvas, điều khiển và bản đồ thu nhỏ: https://reactflow.dev/learn/concepts/built-in-components

## Không gian quản lý gia đình mở rộng

17 mục điều hướng gồm tổng quan, phả đồ, thành viên, chi/cành, tìm quan hệ, danh bạ, phả ký, album, sự kiện, ngày húy kỵ, từ đường, tư liệu, trò chơi, quỹ/vận động, tài sản, đóng góp/nhật ký và cài đặt.

Có thêm/sửa hồ sơ, chọn cha/mẹ và phối ngẫu bằng ID, kiểm tra vòng lặp tổ tiên; lưu trữ và khôi phục hồ sơ không còn được tham chiếu. Tìm quan hệ dùng các liên kết có cấu trúc, không đoán từ tên hoặc nối qua khoảng trống nguồn. Phả ký, tưởng niệm, sự kiện, thu chi, vận động và tài sản có biểu mẫu quản lý. Album nhận JPG/PNG/WebP tối đa 8 MB, gắn người và album.

Xuất phả ký PDF A4 có mục lục và font tiếng Việt, Excel 14 trang tính, CSV danh bạ/thu chi, ICS sự kiện dương lịch. Sao lưu JSON có xem trước và kiểm tra dữ liệu trước khi khôi phục.

Dữ liệu chỉnh sửa lưu riêng trong `data_json/family-state.json`; ảnh ở `data_json/uploads/`; phiên bản trước mỗi lần ghi ở `data_json/snapshots/`. Không ghi đè các JSON nguồn trích PDF. Sao lưu JSON trên giao diện chứa trạng thái quản lý và tham chiếu ảnh, **không chứa nhị phân ảnh, PDF gốc hoặc tệp đóng góp**: sao lưu cả thư mục dữ liệu và tài liệu để chuyển máy đầy đủ. Bố cục canvas lưu riêng trong trình duyệt. Cơ chế revision tránh ghi đè từ hai tab, hàng đợi ghi chỉ hỗ trợ một tiến trình Node. Có thể đặt `FAMILY_DATA_DIR` để dùng thư mục dữ liệu quản lý khác.

Kiểm thử API tích hợp sau khi build: `node scripts/test-family-api.mjs` (cổng 3101, dữ liệu tạm, không sửa dữ liệu gia đình).

Nghiên cứu Phả Tuệ: xem [bảng đối chiếu](docs/phatue-feature-audit.md). Tài nguyên công khai được lưu tại `reference/phatue/`, có manifest URL/hash; ảnh chỉ dùng trong thư viện tham khảo, chưa thay thương hiệu hoặc ảnh tổ tiên. Các dịch vụ tài khoản, AI, thanh toán, mạng xã hội của nền tảng không được chuyển sang dự án này.

## Bổ sung trình biên tập theo mẫu Phả Tuệ

- Tìm người ngay trong cột trái của trình biên tập mở rộng. Kết quả đưa người đó vào tâm nhìn ở mức đọc được, tự mở đường tổ tiên **đã có liên kết**; không đổi gốc hoặc tự nối các gốc tách rời. “Đóng kết quả tìm” trở về nhánh ban đầu.
- Nút tâm ngắm trên ô làm nổi bật tổ tiên và hậu duệ trực hệ; anh/chị/em và các nhánh khác được làm mờ. Nét đứt vàng vẫn nhận diện quan hệ cần đối chiếu.
- Ba kiểu đường nối: vuông góc dùng chung trục con, cong, thẳng. Có khóa vị trí để tránh kéo nhầm. Căn toàn bộ bản vẽ tính cả tiêu đề và khung.
- Xem trước ô của đời được chọn; bật/tắt ảnh hoặc chữ viết tắt, phối ngẫu, ngày sinh/mất và trang nguồn; chỉnh riêng từng đời. Ảnh lấy từ album đã gắn mã hồ sơ, không dùng ảnh mẫu làm tổ tiên.
- Tiêu đề, phụ đề, câu đối hai bên, góc trang trí bản in có thể chỉnh; PDF vector thể hiện các trường và kiểu nối này, nhúng ảnh thật nếu có.
- Chỉ tọa độ do người dùng kéo mới được ghi vào phần vị trí thủ công. Khi đổi số đời, các tọa độ tự động được tính lại để tránh giãn nhánh hoặc chồng ô.

## Trang trí theo lớp trên canvas

Trong **Phả đồ → Mở rộng trình biên tập**, dùng mục **Trang trí** bên trái để thêm hoành phi, cặp rồng chầu, chữ hoặc ảnh. Chọn lớp để kéo trên canvas, kéo nút ở góc phải dưới để đổi kích thước; có nhập tọa độ/kích thước chính xác trong bảng phải. Phím mũi tên dịch 1 px, Shift + mũi tên dịch 10 px. Có phông chữ, căn chữ, màu/nền/viền, độ đậm, khóa/ẩn, thứ tự chồng lớp, nhân đôi và hoàn tác xóa. Tối đa 20 lớp mỗi bố cục.

Nền có trắng, giấy vàng hoặc hoa văn hình học. Ảnh gia đình chọn từ Album; ảnh hoành phi/rồng chầu tham khảo được phục vụ cục bộ từ manifest Phả Tuệ. Không nhận URL ảnh ngoài. **Lưu bố cục** lưu metadata trang trí trong trình duyệt, không nhúng nhị phân ảnh; sao lưu tệp ảnh riêng khi chuyển máy. PDF tính cả lớp nằm ngoài cây, bỏ lớp ẩn, nhúng chữ Việt và ảnh đã chọn.

## Triển khai Dokploy / Nixpacks

Dự án dùng Node.js 22 và npm 10 trở lên. `nixpacks.toml` cố định Node 22, cài bằng `npm ci --include=dev`, build `npm run build`, khởi động `npm run start`. Cổng ứng dụng mặc định 3000, lắng nghe `0.0.0.0`; đặt cổng đích của domain Dokploy tương ứng. Không dùng Yarn cho repository có `package-lock.json` này.

Sau khi cập nhật mã, triển khai lại để áp dụng runtime mới. Phần JSON chỉnh sửa và ảnh tải lên cần ổ lưu trữ bền vững nếu giữ dữ liệu qua các lần tạo lại container; xem phạm vi vận hành và các đường dẫn dữ liệu ở trên.
