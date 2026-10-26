# Quy tắc dựng

## Bắt buộc

- Hash và giữ nguồn; không dùng output cũ làm master khi còn original. Không ghép căn khác hoặc sửa kiến trúc.
- Transcript mỗi câu có id/source_id/in/out/text/complete/listened/reviewer/evidence. Nghe trước/sau cut, giữ đuôi âm, phủ định, số, tên riêng. Không cắt câu để ép thời lượng, không retime giọng tùy tiện.
- Speech mapping1:1: timeline duration bằng source duration. Source span bằng câu/segment nguyên ý đã kiểm tra; không sửa timestamp để lách validator. Giữ raw ASR riêng.
- B-roll có property_id/source span/timeline span và relevance tới lời/claim. Chỉ public amenity được xác minh liên hệ mới dùng ngoài footage căn; không gọi cảnh đường chung là mặt tiền nhà.
- Claim có giá trị/đơn vị/evidence/confirmed_at/confirmed. Mâu thuẫn giá/số phòng/pháp lý: hỏi đúng phần ảnh hưởng hoặc bỏ graphic chưa xác nhận, không mượn thông số căn trước.
- Lời lộ dữ liệu thuộc phạm vi che: báo hai đồng hồ trước mute/bleep. Caption/poster không làm lộ lại.

## Lựa chọn theo job

Hook0–2s có ngữ cảnh và lợi ích thật; A-roll hoặc hình đẹp đúng căn. Không giật giá/diện tích chưa xác nhận. Tour theo logic đi bộ/ý nói: điểm khác biệt → không gian → kết nối → kết; B-roll thử1.5–4s, dài hơn khi cần quan sát, A-roll theo câu. Không quota cut/phút từ reference khác. Rà khoảng không lời dài có mục đích hay thiếu nội dung.

Cut sạch khi đổi ý/không gian, J/L-cut khi lời tiếp tục. Dissolve chỉ khi có lý do, tránh kiến trúc chồng hình. Whoosh theo hướng motion, không mọi cut. Không cùng card/animation ở mọi shot; mỗi graphic có nhiệm vụ khác caption. Kết dùng cảnh hero ổn định, CTA đủ đọc và không cụt câu.

## Thử nghiệm

Crop/grade/font/transition/gain là candidate tới khi xem/nghe file thật. Chạy validate trước dựng và sau thay plan; mapping đúng số học vẫn chưa thay nghe. Sửa lineage/resampling trước tăng sharpen/bitrate.
