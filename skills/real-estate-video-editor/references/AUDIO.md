# Âm thanh có chủ đích

Ledger lưu path/hash/source/author/license evidence/video commercial permission/restrictions/attribution/date. Không lấy nhạc reference hoặc suy quyền từ tênfile. Thiếu nhạc hợp lệ tiếp tục voice+SFX cóquyền; thiếu SFX dùngvoice và báo. Không ép nhạc tổng hợp. Nghe source và candidate trong lời trước chọn nhạc/BPM/genre; waveform không thay nghe. Không có khả năng nghe ghi rõ pending, không gọi đã phối phù hợp.

Pop/click cho keyword/title/marker mộtlần; whoosh cho slide/pan cóhướng; impact cho điểm nhấn thật; riser dẫn tới reveal có payoff. Cue có timestamp/reason/visual_or_keyword/gain/trim/onset. >3cue/5s là cảnh báo thử để nghe lại, không quota. Không rải mọi cut.

**Đo onset thật**: trim đầu im, đặt transient ở event_time bằng cue_at=event_time−transient_offset. Không peak-normalize cảfile rồi lấy .4s đầu như r04; chime18.85s phầnđầu rất nhỏ. Cho tail hợp lý/fade tránhclick. RMS.35s giúp đo masking, không phán chấtâm/click attack.

Helper mix dùng templates/mix.json: voice WAV **đã align toàntimeline**, optionalmusic cùnggốc thời gian, SFX đãtrim. Music `{path,gain_db,permitted,license_evidence}`; SFX thêmat. Sidechain threshold.03 ratio8 attack20ms release350ms là **tham số thử**; nghe pumping/đuôi câu. Sum không normalize từngstem rồi cộng; sample-peak limiter.891 không bảo đảm AAC truepeak. Đo lại file encode. Mẫu music thấp hơn voice12–18dB khi nói; SFX chỉnh theo asset/spectrum, không đồng loạt tănggain.

Mục tiêu social thử −16 tới−14LUFS, ≤−1dBTP sau AAC, không là luật nền tảng hoặc lý do phávoice. `audio` dùng input_i/input_tp; output_* là giả định loudnorm chưa áp. Muốn normalize dùngtwo-pass measuredvalues và nghe lại. Giữ stem/automation.

Nghe tai nghe và loađiện thoại mọicut/cue: đủcâu, không méo/click, ambiance không giật, SFX có nhấn không nuốt phụâm, nhạcduck không pumping; đốichiếu AVsync. Ghi listener/time/artifacthash. ASR/correlation/numeric pass không thay nghe.


## Mặc định dự án: giảm ồn, không nhạc

Theo USER-DEFAULTS.md: voice gốc + SFX, không BGM. Giảm ồn sau khi xác định noise thật: hum/rumble dùng high-pass nhẹ khi cần, noise liên tục thử FFmpeg afftdn theo profile/đoạn noise hợp lệ. Không học noise từ đoạn đang nói và không mặc định noise reduction mạnh cho mọi nguồn. Tiếng xe/giọng người chồng thoại khó tách hơn; báo giới hạn, không hứa loại hết. Chọn đoạn thoại tốt hơn trước khi cố cứu âm xấu.

Giữ stem voice-original và voice-cleaned riêng. Thử đoạn ngắn đại diện; so trước/sau cùng loudness, nghe phụ âm/sibilance/đuôi câu và pumping/musical-noise; giảm mức hoặc bỏ bộ lọc gây mất chi tiết. Không gate cứng cắt hơi, không tự xóa từ. Lưu filter/profile/tham số và timestamp thử; chưa nghe được giữ audition pending, không tuyên bố đã sạch tự nhiên chỉ bằng noise-floor. Có filter không nghĩa xử lý giọng thật đã nghiệm thu.

SFX thư viện `E:/VIDEO/assets/sfx/` chỉ là nguồn ứng viên; vẫn kiểm quyền và onset/trim. Không chèn nhạc để che tiếng ồn. Đo master actualAAC, true peak và headroom cho CapCut, tránh nâng voice/SFX sát0 chỉ để nghe to.
