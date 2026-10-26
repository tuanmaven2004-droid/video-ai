# Đối chiếu thực tế 2026-10-24 — r04 và reference

## Phạm vi và bằng chứng

Đã đọc toàn bộ9 file skill cũ; đọc pipeline inventory/prepare_job liên quan và revise_r03/revise_r04/consolidate_r04/bake_r04_color/mix/qa_r04/check_r03_layout, HTML/timeline thật. Đây là audit skill, không tạo bản video nhà mới. Reference được probe8 file; xem frame samples cả8, lấy dày0.1s template1 đầu và0.2–0.3s video1 hook/map. Không phải xem/nghe liên tục toàn bộ reference. **Chưa nghe trực tiếp** audio: SFX/nhạc hay hơn là phản hồi người dùng, không là kết luận audition của agent.

Artifact ngoài skill dưới `E:/VIDEO/analysis/skill-upgrade-20261024/`: evidence-manifest.json (hash9video), media-probes.json, matched-frames.json, compare-*.jpg, dense-video 1.jpg, dense-template 1.jpg, sfx-measurements.json, *-loudness.log, current-original-probes.json, r04-technical.json. Giữ nguồn và bản xuất cũ nguyên vẹn. Các link tương đối từ case này về workspace là `../../../../analysis/skill-upgrade-20261024/` khi skill được cài đúng chỗ.

| File | Đo trực tiếp |
|---|---|
| video 1.mp4 | 141.802s,720×1280,30fps, video bitrate2.62Mbps |
| r04 | 50.816s,1080×1920,60fps,3048frames, H264/AAC, video bitrate28.16Mbps |
| template1 |52.034s,576×1024,30fps |

Bitrate/raster cao hơn không đồng nghĩa hình cảm nhận nét hơn. Hai video là hai căn/góc quay/ánh sáng khác nhau; không dùng chúng để tính PSNR/SSIM hoặc quy toàn bộ khác biệt cho encoder.

## 1. Hình mềm — quan sát, code và giả thuyết

**Observed_visual:** cặp PNG cùng raster1080×1920 tại r04 25.50s ↔ IMG_2026 source1.18s: chữ/chi tiết bếp và vật nhỏ mềm hơn sau xuất, grade sáng/lạnh hơn. Cặp9.80s ↔ IMG_2016 source1.00s cho thấy tương phản/chi tiết cửa thay đổi và caption chồng vùng dưới; không dùng vùng chữ để đo nét. Cặp4.50s ↔ IMG_2041 source4.85s mặt sáng hơn nhưng chi tiết tóc/da mềm. Không khẳng định toàn video giảm cùng mức; vẫn có chuyển động/khác frame-nearest và grade là biến gây nhiễu.

**Verified_code:** source4K HEVC → proxy1080CRF18 → ghép reel → bakegradeCRF17 → HyperFrames extraction/composite/finalencode. Hai clip còn frame-align reencode. Nhiều generation/resample là rủi ro có thật; chưa ablation để lượng hóa mất mát từng bước. Facegamma.65 và gamma chung1.11 nâng shadow, không thêm chi tiết. Không denoise/sharpen; độ mềm không thể quy cho denoise. Nguồn một số nội thất thiếu sáng/motionblur sẵn có; không thể sửa bằng xuất60. Sourcefps trộn30/60/VFR theo manifest cũ; probe ba bản gốc hiện tại để kiểm lại, sampleVFR chưa chứng nhận toàn clip.

**Fix:** master nguồn gốc, ít generation, scale một lần, correction theo shot, no arbitrary sharpen; bắt buộc so nguồn/xuất aligned ở cùng raster. Chọn fps theo nguồn/mục đích và ghi chính sách lặp frame, không coi60 là nâng nét.

## 2. Chữ yếu và chưa cân — thấy và tính được

**Observed_visual:** video1 0.9–2s headline trắng/vàng có khối tối, nối ranh hình flycam/người dẫn; nền và text được gom thành trọng tâm. r04 1s headline nằm trong card740×494 che hình minh họa, nhãn nhỏ; 10/16/20s lặp script+main+badge/underline ở nền trần sáng. Dòng script trắng mảnh yếu hơn headline, nhiều lớp tranh nhau ý. Có headline lớn trong r04, không kết luận mọi chữ đều nhỏ.

**Measured/code:** lề trái110/phải230 → tâm vùng chữx480 thay vì tâm khung540, lệch60px(5.56%width); là hệ quả safearea bất đối xứng, không lỗi toán học renderer. Nhãn30px chỉ10px khi xem360wide; script64–74px≈21–25px; headline100–150px≈33–50px.12title/50.8s dùng cùng mẫu script, chữ quay, underline;19captioncues. Lint/bounds pass chỉ tránh tràn, không xác minh cân xứng/đẹp.

Template1 0.1–1.2s thấy chữ thay vị trí/rotation/scale, vài lớp được reveal lần lượt, có điểm sáng; không xác định easing/font/plugin chính xác. Template2 cho phân cấp serif/sans/script+icon;template3 số lớn/highlight;template4 lowerthird đỏ. Không nên bê toàn catalogue vào một timeline.

**Fix:** vai trò headline/keyword/subtitle/callout, anchor theo shot, cân quang học, giảm chữ lặp, scrim có chủ đích, phone preview và thời gian đọc.5motion khác nhiệm vụ; không áp mọishot. Token mới là candidate, không hứa giống reference chính xác.

## 3. SFX thiếu nhấn — đo được, chưa nghe

**Measured:** finalr04 −17.82LUFS/−2.80dBTP/LRA4.20; video1 −14.10LUFS/−0.25dBTP/LRA2.80. Chênh3.72LU integrated không là mức SFX riêng, không lý do nâng mọitrack3.72dB. Peak reference sát0 không phải mục tiêu cần sao chép.

R04 có11cue, không phải không cóSFX. Script mix normalize peakasset rồi truncate thời lượng chung: impactpeak≈−20,whoosh−18,pop/click−16dBFS. Đo stem cửa sổ0.35s ở6.09:whooshRMS−32.94 vsvoice−19.32(−13.62dB);14.70:click−41.19 vsvoice−20.25(−20.94dB);18.85:chimepeak−57.05,RMS−66.94 vsvoice−20.21(−46.73dB). Số này từ stem **trước mastergain**; không gọi là isolatedSFX củaAAC. Peak normalize toànasset không bảo đảm attack của đoạn cắt mạnh; chưa đo offsettransient toànfile/chưa nghe nên masking và chất âm vẫn inferred.

**Fix:** cue theo event/keyword, trim silence và onset, gain theo asset, nghe A/B cùngvoice trên phone. Giữ stem/ledger, sidechain music, đo actualAAC truepeak. Không chữa bằng rải thêmwhoosh hoặc ép track đều to.

## 4. Thiếu bản đồ

**Observed_visual:** video1 ~12s có pin/label trên flycam;98.8–100s có card bản đồvệ tinh/pin;100.3s bắt đầu đổi về card cảnh kênh. Chưa xác minh có overview→zoom trong khoảng trước đó, provider/license hay tọa độ thật; không tự gán GoogleMaps license cho ảnh. video3 sample20s có mapcard+route+6phút/1.6km và dòng nguồn; nhìn thấy không xác nhận số là đúng/được phép sao chép.

**Verified_code:** r04 timeline/HTML không có basemap/pin/route component;35.98s chỉ title tên đường,40.38–44.42s nhãn tiện ích và B-roll, không phải motionmap. Thiếu confirmed publiccoordinates và mapasset/license trong job là thiếu input, không lý do tự đoán pin.

**Fix:** helper map offline overview→zoom→pin→label→optionalroute, publicprecision và evidence gate. Test với tọa độ/ảnh giả lập rõ làfixture, không căn ALD. Chưa tích hợp HyperFrames adapter end-to-end hoặc providerAPI. Không fetch tile công cộng hay lấymapreference.

## Các giới hạn còn lại

R04 decode toàn file lại đạt, không có ứng viên black/freeze ở ngưỡng test; codec/size/fps đúng. Điều này không chứng nhận sync bằng tai, motion đẹp, privacy toànframe hoặc tiêu đề dễ đọc. Không xác nhận che hết số nhà/biển số/biển quảng cáo; các frame đường phố mẫu vẫn có chữ/xe theo scope job trước. Privacy của skill mới phải làm lại theo brief căn mới.
