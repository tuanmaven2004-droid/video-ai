# Runtime thực tế — snapshot 2026-10-24

Đã chạy doctor mới: `E:/VIDEO/analysis/skill-upgrade-20261024/environment-upgraded.json`. Không cài hoặc cập nhật dependency trong nhiệm vụ này.

| Runtime | Trạng thái thực |
|---|---|
| Python3.12.14 | chạy helper/tests |
| Node24.22.1 | chạy CLI version/browser tests |
| HyperFrames0.8.162 | package/version thực khớp; chưa render composition mới |
| FFmpeg6.1.1 / FFprobe4.0.2 | probe/decode/filter/mix/mask fixture và file actual |
| ChromeHeadless152 / puppeteer-core | 5motion và map seek tests thực; cần quyền kết nối loopback khi sandbox chặn |
| numpy2.5.4/Pillow13.0.0 | dùng audit frame/audio; toolkit production chủ yếu stdlib+FFmpeg |
| faster-whisper1.2.1, ONNXRuntime1.31.0, RapidOCR1.4.4, OpenCV5.0.0.93 | tìm thấy tại workspace .hyperframes-tools/python-asr; không rerun ASR/OCR/tracker nhà thật trong lần nâng cấp |
| Tesseract/WhisperCLI | không thấy trênPATH; không nghĩa không cópackage Python |

Tại máy hiện tại Python `C:/Users/tuann/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`; Node cùng dependencies/node/bin/node.exe; FFmpeg/FFprobe trong `.hyperframes-tools/node_modules/ffmpeg-static` và `ffprobe-static/bin/win32/x64`. Chuyển máy dùng PATH hoặc env FFMPEG/FFPROBE; không hardcode các userpath vào job mới. Doctor chỉ tìm module/model/executable, không chứng nhận end-to-end.

Chỉ3 bundled skill tìm thấy: hyperframes,hyperframes-cli,media-use tại `.hyperframes-tools/node_modules/hyperframes/dist/skills/`. Không còn pluginbundle cũ. Sáu skill chưa thấy: general-video,hyperframes-core,hyperframes-animation,hyperframes-keyframes,hyperframes-creative,hyperframes-audio. Nếu cần đề xuất nguồn chính thức [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes), chọn tag/revision tương thích, không cài trùng hoặc dùng API mới trên runtime cũ. npx/npm chưa có trênPATH; wrapper `hyperframes.cmd` dùng pin hiện tại. Không chạy latestupgrade vì yêu cầu user cấm tự cập nhật chưa cần thiết.

Khi authoring: đọc contract bundled CLI rồi `hyperframes.cmd --help` / subcommandhelp phiên bản thật. Skillrouter upstream mới nhắc core chưa cài không làm core tự có; báo thiếu contract/chọn adapter đãkiểmchứng thay vì đoán flags. Snapshot r04 đã render trước không là chứng nhận mọi API mới. Canonical live grading r04 timeout cả24và3media, fallback offlinegrade hoạt động lịch sử; không khẳng định nguyên nhân GPU hoặc gọi timeoutpass.

Không tích hợp provider bản đồ/geocoder, không APIkeys hoặc quyền nghe trực tiếp. Maphelper nhận assetlicenced offline và confirmedpublicinput. OCR/detector tự động nhà thật, tracking qua occlusion, lipsync/listening/phoneUI thật cần kiểm định job; maskhelper chỉ nội suy bbox thủ công trênCFR.
