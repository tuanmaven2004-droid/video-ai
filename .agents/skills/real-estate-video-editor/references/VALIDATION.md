# Kiểm định skill — 2026-10-24

## Đã chạy

- Test scripts/test_tools.py: **24 bài đạt** tại `E:/VIDEO/analysis/skill-upgrade-20261024/tests-final/tests.json`. Fixture tổng3giây180×320, không render video nhà.
- Probe thật metadata/hash/audio/rotation; VFR sample; emptyjob vẫn pending; reject cắt câu/sai căn/claim thiếu/asset không quyền/privacy verified thiếu chứng cứ.
- Decode/codec/fps/size fixture; bắt ứng viên black/freeze; aligned frame comparison PNG giống nhau; refuseoverwrite.
- Mix WAV thử với sidechain, đo background tần số160Hz giảm khi có testvoice800Hz; đây là testtone, **không phải nhạc/SFX xuất cho người dùng**. Chưa audition.
- Opaque moving mask từ keyframes thủ công: đúng90frame, pixel đen đúng vị trí nội suy, giữ hashsource, trạng thái luôn needsallframereview; refuseoverwrite.
- Browser thực:5motionroles, fontload và bounds, seek tiến/lùi; map pin+POI+route hiện, seek0→4→1→4 deterministic. Lỗi exportmarker map banđầu đã được sửa và test thêm pointcount/visibility; bản cuối kiểm thành công.
- Probe8reference và r04, xem contact/denseframes,3cặp source/export PNG; SFXstem/loudness; decode r04toànfile, không đen/freeze ứng viên với black.1s/freeze1s ngưỡng hiện tại. Bằngchứng/caveat ở CASE-STUDY.

Kết quả quick_validate, linkcheck, CLIhelp, compile, backup và installhash nằm trong `E:/VIDEO/analysis/skill-upgrade-20261024/skill-validation.json` sau bước hoàn tất. Quickvalidator kiểmfrontmatter/scaffold, không chứng minh chất lượng dựng.

## Chưa hoạt động end-to-end / vẫn thủ công

Không rerun ASR/OCR/autoobjecttracker trên footage nhà; package có không là readiness. Maskhelper không tự phát hiện/chọn đối tượng, không hỗ trợ VFR/HDRpreservation. Không nghiệm thu che mọiframe của r04 hoặc nhàmới. Kiểm phảnchiếu/audio/caption, transition và encode vẫn cần người/agent xem được actualmedia.

Không nghe bằng tai reference/r04/mix mới; waveform, loudness, correlation hoặc testtone không xác nhận voice clarity/nhạcphùhợp/SFXhay. Chưa kiểm appTikTok thật; mock/bounds chỉ hỗtrợ. Chưa tíchhợp map/motion vào job HyperFrames mới và render end-to-end; browser component test không thay điều đó. Basemapprovider/API/license/newpubliclocation là đầu vào job, không giả có.

## Checklist file giao thật (job mới)

1. Probe codec/aspect/size/SAR/fps/color/audio/duration; decode toànfile, xem ứng viên black/freeze để phân biệt hold/fade chủđích. Nguồn hashtrước/sau khớp.
2. So frame nguồn/xuất aligned; rà hình mất/đứng, resample/HDR/skin/halos và hai phía cut; fps đúng không đồng nghĩa nét.
3. Nghe mọi cut nguyêncâu, kiểmsync đầu/giữa/cuối và các retime; SFX/cue/duck/loudness/truepeak actualAAC, phone vàtai nghe.
4. Xem fontViệt/headline/subtitle/safeUI/readingtime/motionseek trên phone-size; title nổi và cân, không chỉ bounds pass.
5. Privacy scan toàntimeline, mọiframe khoảng nhạy cảm, reflection/background/audio/caption/transition/encode; lưu reviewer/time/artifacthash và phần chưa chắc, không `safe:true`.
6. Claim/POI/route/license/attribution đúnginputxácnhận. Báo timestamp unresolved; không tự đánh manualpassed hoặc giao như đã kiểmđủ.


Chạy lại test khi đổi helper: `python scripts/test_tools.py --workspace <workspace> --out <thư-mục-test-mới>`. Chỉ sinh fixture tối đa3s, không cần nhà thật. Browser evidence ở thư mục audit là thử riêng trên Chromium; script test Python không tự hứa đã kiểm motion trong trình duyệt.
