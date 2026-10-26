# Thumbnail bất động sản

Dùng khi người dùng muốn ảnh bìa/thumbnail đi cùng video review. Học thứ bậc chữ và tương phản từ ảnh tham chiếu; không bê logo, ảnh nhà hoặc tài sản của listing khác.

## Chọn ảnh và nội dung

- Chọn khung rõ từ footage/photo của đúng căn. Xem ảnh trước khi đặt chữ; ưu tiên khung không có mặt tiền bị chủ nhà hạn chế công khai, chữ/biển nhạy cảm, rung hoặc chủ thể bị cắt.
- Dùng đúng thông tin người dùng cung cấp hoặc đã xác minh trong brief. Không tự thêm diện tích, số phòng, pháp lý, tiện ích, khoảng cách, địa chỉ hay “ở liền”. Nếu người dùng đưa câu chữ cụ thể, giữ nguyên.
- Nếu người dùng đưa mẫu có tỷ lệ 3:4, dùng 1080×1440 làm khung mặc định. Với tỷ lệ khác, theo yêu cầu job; không gọi mọi kích thước là chuẩn nền tảng.

## Bố cục hiện có

`assets/Anton-Regular.ttf` (OFL) cho tag/headline condensed. Mẫu của script: nền ảnh thật; gradient tối gọn ở vùng dưới; pill viền vàng cho tag; địa điểm và giá cùng một hàng (địa điểm trắng, giá vàng); thông số ở hàng dưới; nét đen và bóng nhẹ. Đặt cụm chữ hơi cao hơn vùng đáy để cân bố cục; chừa khoảng cách rõ giữa pill, headline và thông số. Giữ lề tối thiểu4.5%, fit chữ thay vì cắt, và không che mặt/đặc điểm căn nhà quan trọng. Đây là một preset có thể thay đổi theo ảnh, không phải bố cục bắt buộc cho mọi căn.

Script `scripts/thumbnail.py` nhận một still đã chọn, vẽ ba dòng và ghi ảnh PNG mới; từ chối ghi đè. Nó dùng Pillow và font Anton trong `assets/`, không tạo cảnh bằng AI. Ví dụ:

```text
python scripts/thumbnail.py --source E:/VIDEO/jobs/<job>/selected-still.png --output E:/VIDEO/output/<new-thumbnail>.png --tag "NHÀ ĐẸP Ở LIỀN" --location "HUỲNH TẤN PHÁT" --price "5,7 TỶ" --details "3 × 16 M · CN 47 M²"
```

Canvas mặc định1080×1440; chọn `--width`/`--height` theo brief. Ảnh gốc chỉ đọc. Khi ảnh được crop sang tỷ lệ khác, kiểm tra crop thật và không phóng ảnh nguồn thấp lên mà giấu mất suy giảm.

## Kiểm tra

Mở PNG thực và xác nhận dấu tiếng Việt, dòng chữ, giá, tương phản ở kích thước nhỏ, crop, chi tiết căn nhà và privacy trong chính still đã dùng. Ghi rõ nếu chưa rà nền/biển/phản chiếu; việc chọn một frame sạch không chứng minh cả video đã sạch. Metadata quyền ảnh/nhạc không liên quan đến ảnh do người dùng cung cấp; giữ attribution/điều kiện nếu thêm asset ngoài.


