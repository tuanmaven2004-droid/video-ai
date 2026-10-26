# Nguồn, màu, nét và fps

Probe lưu stream/format/hash/rotation/display size/bitrate/pix_fmt/primaries/transfer/matrix/range/audio. FFmpeg vfrdet **12s đầu** chỉ sample; phải chạy toàn clip/đọc full PTS trước kết luận CFR/VFR. r_frame_rate khác avg không đủ kết luận. FFprobe4.0.2 có thể thiếu side-data codec mới; unknown không đồng nghĩa SDR.

Chọn take bằng focus/motion blur/rung/exposure/noise và giá trị nội dung, không bitrate/fps đơn lẻ. Lineage nguồn → xử lý → intermediate → renderer → encode: ưu tiên nguồn gốc ở final, gom grade/redact/crop/scale một lượt. Nếu renderer cần intermediate, chọn lossless/near-lossless tương thích và kiểm performance. Proxy nhỏ chỉ offline phải relink master. Bitrate output cao không khôi phục chi tiết mất. Ghi JPEG extraction/chroma/resampling của renderer khi có.

Rotation một lần; crop theo display size. Ghi upscale ratio từ source crop tới output visiblepixels; >1 xem detail và lý do. Không phóng giãn nhà. So cùng raster/timestamp, không lấy4K source100% so1080 output100% rồi kết luận.

| Tình trạng | Quyết định |
|---|---|
| HDR/LOG | Xác minh transfer/gamut/profile rồi transform/tone-map về đích; gắn tag bt709 không chuyển màu. Kiểm highlight/skin, thiếu metadata hoãn grade mạnh. |
| Thiếu sáng | Nâng exposure/shadow vừa phải từng nhóm; face feather tracking có kiểm tra. Không mặc định gamma.65 của ALD. |
| Cháy sáng | Bảo vệ highlight còn dữ liệu; không hứa khôi phục chi tiết mất hoặc tự thay trời. |
| Cast | WB theo môi trường/vật trung tính, giữ đèn ấm có chủ đích; không gray-world mù quáng. |
| Noise | Denoise khi cần, thử chuyển động tóc/gạch/vải; từ chối wax/ghost. |
| Sharpen | Sau scale/correction, radius/amount nhỏ thử crop; từ chối halo/noise. Laplacian không điểm chất lượng. |

FPS theo trục thoại/chuyển động/mục đích:25/30 thường cùng nhịp,50/60 giữ khi nguồn và nội dung có lợi.30→60 chỉ repeat/interpolate, không thêm nét; optical flow có thể méo tay/lan can. Mixed/VFR ghi chính sách resample, kiểm sync đầu/giữa/cuối. CRF17–20 là khoảng thử, không chuẩn bảo đảm. MP4 H264/AAC yuv420p SAR1 theo brief; độ phân giải không chứng minh chi tiết.

`compare` dùng templates/compare.json, PNG sau autorotate+scale chung; crop là w:h:x:y sau scale. Mapping phải đúng, reframe khác cần sửa vùng so hoặc bỏ cặp sai. Không dùng SSIM/PSNR khi khác grade/overlay/crop/motion. Xem fine detail/halos/noise/skin/contrast ở100% rồi360×640. Ít nhất một shot mỗi nhóm nguồn/grade, mọi xử lý mạnh và hai phía transition. Suy giảm rõ thì sửa lineage/resampling trước sharpen. Đo codec PSNR/SSIM chỉ khi input/output aligned cùnggrade.


Probe gốc có thể chứa GPS/creation metadata riêng tư: chỉ lưu trong hồ sơ nội bộ, không đưa nguyên manifest lên mạng. Final strip metadata không cần thiết (ví dụ `-map_metadata -1`), giữ/ghi color tags chính xác sau transform; probe lại final để tìm location/address tags, không chỉ xem hình.
