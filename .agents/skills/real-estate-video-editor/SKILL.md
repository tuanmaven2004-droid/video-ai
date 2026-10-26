---
name: real-estate-video-editor
description: Dựng và kiểm định review bất động sản bằng HyperFrames từ footage thật; có thể tạo thumbnail từ khung hình chính căn nhà. Giữ lời gốc, B-roll đúng căn, typography, âm thanh và dữ kiện có nguồn; không tạo cảnh nhà giả.
---

# Real estate video editor

Thực thi theo brief từng căn. Không kế thừa giá, địa chỉ, quyền công khai hoặc đồng ý từ job khác. Khi chỉ phân tích/nâng cấp skill, không render video. Phân biệt `observed_visual`, `measured`, `heard`, `inferred`, `proposed`, `unknown`; gắn file/timestamp/phương pháp. ASR/waveform không là bằng chứng đã nghe.

## Mặc định của chủ dự án

Đọc [USER-DEFAULTS.md](references/USER-DEFAULTS.md). Khi người dùng gửi nguồn để dựng, tự thực hiện bản đầy đủ, không chờ preview trung gian. Mặc định giảm ồn giữ giọng gốc tự nhiên, voice + SFX từ E:/VIDEO/assets/sfx/, **không nhạc nền**, MP4 dọc4K2160×3840 để thêm nhạc trong CapCut. Chỉ dẫn mới của từng job được ưu tiên; nguồn gửi chỉ để phân tích không là yêu cầu render.

## Khởi động

1. Đọc chỉ dẫn dự án và yêu cầu hiện tại. Chạy `scripts/doctor.py --workspace <workspace> --output <report-mới.json>`. Đọc [phụ thuộc](references/DEPENDENCIES.md) trước tích hợp; không cài trùng/tự cập nhật. Đọc hyperframes, hyperframes-cli, media-use thực có; không tuyên bố gọi skill thiếu.
2. Chạy `scripts/video_tools.py init <job-mới> --property-id <id>`. Điền [hồ sơ và lệnh](references/WORKFLOW.md). Nguồn chỉ đọc, output tên mới. Thiếu reference thì hỏi file và tiếp tục probe, không đoán phong cách.
3. Đọc [STYLE-GUIDE.md](STYLE-GUIDE.md), [EDITING-RULES.md](EDITING-RULES.md); chọn profile theo reference và brief mới. [Case r04/video 1](references/CASE-STUDY-R04.md) là bài học có giới hạn, không preset cho mọi căn.

## Đọc theo công việc

| Việc | Tài liệu / công cụ |
|---|---|
| Chọn nguồn, fps/HDR, màu, nét | [QUALITY.md](references/QUALITY.md); video_tools.py probe / compare |
| Ảnh thumbnail | [THUMBNAILS.md](references/THUMBNAILS.md); scripts/thumbnail.py — khi brief yêu cầu ảnh bìa |
| Nguyên câu, mapping, B-roll | [EDITING-RULES.md](EDITING-RULES.md); transcript + shot list + edit plan |
| Chữ/safe area/motion | [TYPOGRAPHY.md](references/TYPOGRAPHY.md); templates/design-tokens.json, typography.css, motion.js |
| Cue/ducking/loudness/nghe | [AUDIO.md](references/AUDIO.md); video_tools.py mix / audio |
| Bản đồ vị trí | [MAPS.md](references/MAPS.md); scripts/map_component.py |
| Mask và lời/chữ nhạy cảm | [PRIVACY.md](references/PRIVACY.md); privacy-review theo khoảng; scripts/mask_keyframes.py cho bbox thủ công |
| File thật và giao | [VALIDATION.md](references/VALIDATION.md); video_tools.py validate / qa |

## Cổng bắt buộc

- Giữ giọng gốc, nguyên ý và câu; khóa in/out sau nghe hoặc transcript người có thẩm quyền đã kiểm tra. Không AI voice, nhà giả, sửa kiến trúc hoặc B-roll khác căn. Không tự thêm giá/diện tích/pháp lý/tiện ích; claim có nguồn và mức xác minh.
- Asset nhạc/SFX/map/font có quyền và ledger. Thiếu nhạc hợp lệ vẫn tiếp tục voice + SFX hợp lệ; thiếu cả SFX dùng voice và báo thiếu. Không lấy tài sản reference.
- Privacy theo phạm vi user của job; OCR âm tính không chứng minh an toàn. Thoại lộ dữ liệu cần che: báo source/timeline timestamp trước xử lý theo hướng dẫn thật.
- Chủ dự án đã yêu cầu tự dựng đầy đủ khi gửi nguồn; không chờ preview trừ khi brief mới yêu cầu preview. Chỉ hỏi dữ kiện thực sự ảnh hưởng nội dung hoặc khi không thể tiếp tục, tự quyết các lựa chọn dựng thông thường. Chưa có vị trí được phép công khai thì hoãn map, tiếp tục phần độc lập.
- Check/lint pass không chứng minh đẹp, nét, nghe rõ hoặc đã che hết. Đối chiếu nguồn/xuất cùng raster, xem phone, nghe cut/cue, kiểm mask qua transition/encode. Chưa kiểm tra đủ giữ pending và timestamp, không tự đánh passed.

Xuất MP4 H.264/AAC, mặc định dọc4K2160×3840 khi brief không chọn khác; fps theo nguồn/mục đích, không mặc định60. Báo file mới, đã kiểm gì, chưa xác minh và timestamp. Không tự upload.
