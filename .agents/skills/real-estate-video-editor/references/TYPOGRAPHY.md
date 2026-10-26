# Hệ chữ và motion

Font phải có license và glyph Việt thật. Anton phù hợp condensed uppercase khi brief chọn; subtitle có thể sans dễ đọc đã cài và có quyền. Script chỉ accent ngắn, không dùng cho giá/pháp lý/phụ đề. Render thử “Ắ ấ ễ ự Đ ỷ m² 4,2” với font đã load; tên CSS không chứng minh glyph.

Tokens là điểm bắt đầu cho1080×1920, **không số đo reference**: headline92–144px (8.5–13.3% width), keyword110–172px, subtitle54–64px, callout44–58px; tối đa2 dòng, hook≤8 từ. Nếu dài chia cue/biên tập đúng ý, không shrink thông tin chính xuống nhãn30px. Một headline+subtitle phần lớn là đủ; bỏ badge/underline không thêm nghĩa. Không lặp cùng câu ở ba lớp.

Safe area theo job/UI thật: thử lề đối xứng8%, top10%, bottom22%, subtitle y65–74%; vùng nút phải/description cần mock riêng. Đây không là chuẩn TikTok cố định. Headline căn tâm hìnhx540 nếu không vướng, subtitle có thể căn vùng đọc; ghi anchor và kiểm cân quang học, không dồn tất cảx480 như r04. Xem360×640 với overlayUI và nền thật; chưa test app thật ghi simulated. Tránh mặt/chủ thể/cửa/chi tiết kiến trúc; xung đột thì chuyển chữ/giảm chữ.

Trắng/amber cần nền đủ tương phản; nền sáng/rối dùng scrim cục bộ hoặc vị trí khác. Shadow/stroke hỗ trợ, không thay bố cục. Mục tiêu thiết kế contrast≥4.5:1 kiểm tại nền xấu nhất, không suy từ token. Hold đọc thử max(1.2s,sốtừ/3), subtitle≤17ký tự/s; arrival/exit không tính hold, đồng bộ ý nói.

`templates/motion.js`: REMotion.mount(gsap,element,role,duration) trả timeline paused; element có data-main và optionaldata-sub. Khi nested vào master phải unpause child, đăng ký master theo contract CLI thật; không dùng autoplay/timer. Kiểm seek đảo. CSS dùng font REHeadline/RESubtitle cần @font-face của job.

| Role | Mẫu tự thiết kế | Mục đích |
|---|---|---|
| hook | lift28px+scale.92→1,.32s | lời hứa đầu |
| space | slide30px,.24s | đổi không gian, không mọishot |
| stat | scale1.12→1,.30s | số đã xác nhận, không fake count-up |
| amenity | lift18px,.28s | POI/kết nối thật |
| closing | fade.32s | CTA với hình đẹp |

Hold rồi exit.16s, điều chỉnh job. Không cùng animation/card toàn timeline. Stagger dùng grapheme giữ dấu Việt và chỉ tại điểm nhấn; không chữ bay mọi caption. SFX theo settle/impact có bù onsetasset. Kiểm start,.1/.2/.4s,hold,exit,cả hai phía cut và seek ngược; bounds/glyph/fontloading/phone review. Test mẫu không thay kiểm composition thật.
