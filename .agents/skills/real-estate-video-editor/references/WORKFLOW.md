# Hồ sơ và thực thi

Python3.10+; `python` bên dưới là interpreter doctor đã xác minh. Truyền workspace trước subcommand, hoặc env FFMPEG/FFPROBE là executable thật. Helper không tự cài. Output helper từ chối ghi đè; doctor có thể thay report được chỉ định.

```text
python scripts/doctor.py --workspace E:/VIDEO --output <new-environment.json>
python scripts/video_tools.py init <new-job> --property-id <id>
python scripts/video_tools.py --workspace E:/VIDEO probe <a.MOV> <b.MOV> --out <probe.json>
python scripts/video_tools.py validate <job> --out <validation.json>
python scripts/video_tools.py --workspace E:/VIDEO compare <compare-spec.json> --out <new-frame-dir>
python scripts/video_tools.py --workspace E:/VIDEO mix <mix-spec.json> --audio-out <new-mix.wav> --out <mix-report.json>
python scripts/video_tools.py --workspace E:/VIDEO audio <actual.mp4> --out <loudness.json>
python scripts/video_tools.py --workspace E:/VIDEO qa <actual.mp4> --expected <expected.json> --out <technical.json>
python scripts/map_component.py <map-spec.json> --out <new-map-dir>
```

Init tách templates/job.json thành9 hồ sơ version1.0; array trống nghĩa chưa làm, không passed.

| Hồ sơ | Contract record |
|---|---|
| brief | source_roots/reference_files, target, claims `{id,value,unit,confirmed,evidence,confirmed_at}`, privacy/public_location, user_authorization thật |
| source-manifest | merge probe records, thêm `{id,property_id,role,duration,relationship_verified}`; role public_amenity phải xác nhận quan hệ; giữ hash/path/probe |
| shot-list | shots `{id,source_id,in,out,space,motion,quality_observation,relevance,claim_ids,privacy_risks,decision,reason}` |
| transcript | engine/model, sentences `{id,source_id,in,out,text,complete,listened,reviewer,evidence}`; raw ASR riêng |
| edit-plan | duration,fps,fps_reason; visuals `{id,source_id,source_in,source_out,timeline_in,timeline_out,relevance,crop,grade,mask_ids}`; speech cùng mapping thêm sentence_id; graphics `{id,role,text,factual,claim_ids,timeline_in,timeline_out}`; transitions `{at,duration,type,reason}`; encode_lineage |
| cue-sheet | cues `{id,asset_id,type,at,duration,reason,visual_or_keyword,gain_db,asset_trim_in,asset_transient_offset,listened_in_mix}` |
| asset-ledger | assets `{id,path,sha256,source,author,license,license_evidence,permitted,restrictions,attribution,accessed_at}` |
| privacy-review | status,artifact_sha256,full_timeline_scanned,reviewer; intervals `{id,source_id,source_in,source_out,timeline_in,timeline_out,coordinate_space,keyframes,method,status,all_frames_reviewed,encode_checked,reviewer,evidence,unresolved}`; audio_disclosures hai đồng hồ |
| qa-report | technical trỏ report file thật; manual từng vai trò `{status,evidence,reviewer,artifact_sha256,timestamps}` |

Validator kiểm một số invariant quan trọng, không JSON Schema toàn diện hay chứng nhận nội dung. Exit2 khi errors/pending, tách riêng. Không tự điền listened/confirmed/reviewer để vượt cổng. qa exit2 khi technical lỗi hoặc black/freeze ứng viên; exit0 chỉ technical, chưa giao tự động.

Thứ tự: probe/xem/nghe → transcript+claim+shot list → mapping/style/cues/validate → dựng HyperFrames bằng contract phiên bản thật → preview hoặc full theo quyền job → qa file thật, compare, phone/listen/privacy → hash nguồn sau và báo cáo. Thiếu map không ngăn dựng phần độc lập. Không full render chỉ test skill.


## Thumbnail (khi brief yêu cầu)

Chọn một still sắc nét từ footage của đúng căn, xác nhận crop và privacy trên ảnh đó, rồi dùng `scripts/thumbnail.py` với đúng ba dòng tag/khu vực/giá có trong brief. Mặc định mẫu tham chiếu 3:4 xuất 1080×1440; lấy một tỉ lệ khác nếu brief hoặc nền tảng yêu cầu. Script chỉ crop nhẹ, cân sáng/màu vừa phải và vẽ chữ; không tạo hoặc sửa kiến trúc. Đọc [THUMBNAILS.md](THUMBNAILS.md), xem ảnh xuất thật, giữ file nguồn và không ghi đè thumbnail cũ.
