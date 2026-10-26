# Phát hiện, tracking và kiểm tra che thông tin

Ghi phạm vi dữ liệu cần che trong brief. Mặc định tìm biển số, số nhà, địa chỉ, điện thoại, biển quảng cáo và nhận diện khác đã nêu; không suy ra danh tính không quan sát được.

## Phát hiện

Quét đầu/giữa/cuối shot và tại cut/pan/zoom, mở cửa, gương/kính/màn hình, vật di chuyển. OCR mẫu chỉ tạo ứng viên: dùng đa tỷ lệ/rotation khi chữ nhỏ/nghiêng, đối chiếu bằng mắt. Detector bổ sung vì chữ có thể không đọc được; model tổng quát không mặc nhiên có class biển số/số nhà. Xác minh class/trọng số thật. Kiểm tra cả audio/transcript, caption, poster và metadata.

## Mask theo thời gian

- Ghi source_id, source in/out, bbox/keyframes trong hệ pixel sau rotation/crop và kích thước frame; chuyển tọa độ khi scale/reframe. Không đồng nhất source time với timeline time.
- Phát hiện lại khi đổi góc/occlusion/camera cut/motion blur hoặc tracker mất đối tượng. Không nội suy xuyên cut hay che khuất mà không kiểm tra.
- Nới vùng và thời gian để bao chữ lúc rung/blur. Bắt đầu trước frame đầu có thể đọc, kết thúc sau frame cuối; padding cố định không thay kiểm tra.
- Blur đủ mạnh, mosaic hoặc mask đặc; còn đọc được thì đổi cách che. Không dùng blur toàn khung để tuyên bố theo dõi riêng biển số.
- Ưu tiên bake redaction vào proxy rồi composite trong HyperFrames. B-roll/transition/thumbnail dùng proxy đã che; không để lớp gốc lộ qua opacity, crop hoặc crossfade.

## Coverage và bằng chứng

`privacy-review.json` của job ghi source_id, category, source in/out, hệ tọa độ và bbox/keyframes, tool/version/model, mask, frame đã rà soát, phương pháp/người kiểm tra, mất track, timestamp chưa giải quyết và artifact/revision đã xem.

Trạng thái: `candidate_detected`, `mask_applied`, `verified_for_reviewed_interval`, `needs_manual_review`. Không đặt `safe: true` cho toàn video từ vài ảnh mẫu.

Kiểm tra **mọi frame của từng khoảng nhạy cảm** ở fps/độ phân giải xuất, bao gồm rìa mask, phản chiếu, nền, transition và file MP4 encode. Automation coverage chỉ hỗ trợ; phải xem bằng chứng. Nếu chưa biết đầy đủ khoảng xuất hiện, quét dày/toàn shot và xem chuyển động; không tự cấp verified. Preview không thay kiểm tra toàn timeline.

Ghi timestamp, lý do không chắc và hành động cần làm. Còn nghi ngờ thì giữ nội bộ, loại shot/crop hoặc nhờ kiểm tra thủ công; không giao final như bản đã ẩn an toàn. Nếu thoại đọc thông tin cần che, xin chỉ dẫn bleep/mute đoạn đó, giữ nguyên các lời khác.

## Thiếu công cụ

OCR có thể dùng Tesseract (+ ngôn ngữ phù hợp), PaddleOCR/EasyOCR; tracking có thể dùng OpenCV với detector/class/trọng số phù hợp. Đây là lựa chọn, không phải xác nhận đã cài hay đạt độ chính xác. Package tồn tại không chứng minh model sẵn sàng. Báo thiếu trước, đề xuất cài theo quyền job hoặc mask thủ công có rà soát từng frame.


## Helper mask có thể chạy

`python scripts/mask_keyframes.py <spec.json> --workspace <workspace> --out <new-master.mkv>` chỉ áp **mask đặc từ bbox thủ công**, nội suy tuyến tính trong cùng shot; không là automatictracking/OCR/detector. Không nội suy qua cut/occlusion: chia interval và thêm keyframe đã rà. CFR phải được xác minh toàn clip, VFR/HDR không được giả hỗ trợ; decode autorotate RGB có thể đổi màu nên nguồnHDR cần adapter riêng và comparison.

Spec: `{source,coordinate_space:"autorotated_display_pixels",display_size:[w,h],fps:"30/1",cfr_verified:true,intervals:[{in:0,out:2,padding:12,keyframes:[{t:0,bbox:[x,y,w,h]},{t:2,bbox:[x,y,w,h]}]}]}`. Keys bao đầu/cuối khoảng, sourceaudio copied **không che lời**. Output FFV1losslessMKV là master dẫn xuất, không finalMP4, dunglượng lớn; giữ lineage khi relink. Báo frames/maskedframes/hash và luôn mask_applied_needs_all_frame_review. Test90frame chỉ chứng minh mask math/encode, không phát hiện hết dữ liệu riêng tư.
