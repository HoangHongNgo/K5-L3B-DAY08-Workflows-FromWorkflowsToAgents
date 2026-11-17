# Báo cáo cá nhân — Trần Việt Anh

## 1. Thông tin thành viên

- Họ tên: Trần Việt Anh
- MSSV: 2A202604029
- Email/GitHub: chưa xác nhận trong `TEAM.md`

## 2. Phần việc phụ trách

Shape C `orchestrator`, gồm hai checkpoint:

- **CP2:** thay stub trong `src/lab8/shapes/orchestrator.py` bằng luồng orchestrator + investigator chỉ đọc, cùng chữ ký `run_claim` với các shape khác.
- **CP3:** handoff không mang secret qua ranh giới agent, và ghi tiền an toàn khi gọi lại hoặc khi crash.

## 3. Đóng góp cụ thể

Commit `6a6dbe8` ("CP2, CP3 orchestrator") chỉ sửa một file, `src/lab8/shapes/orchestrator.py` (+109/−6). Luồng xử lý một claim:

1. Đọc claim bằng `get_claim_view` (chỉ field cho phép, không có `parent_secret` hay `raw_headers`). Claim không tồn tại thì trả `failed`.
2. Thiếu `order_id` thì trả `needs_info`, không ghi ledger. Không lấy mã đơn từ câu chữ trong ticket.
3. Dựng handoff bằng `lab8.handoff.make_handoff` với `facts = {}` và chỉ ba tool đọc (`lookup_order`, `lookup_policy`, `compute_compensation`). Trace ghi handoff đã sanitize, không ghi parent context.
4. Chạy `run_readonly_investigators`. Đơn không tìm thấy hoặc không thuộc principal thì trả `escalated`, không lộ dữ liệu đơn.
5. Lấy quote từ `compute_compensation` trên dòng order trong DB, không dùng số ngày ghi trong ticket. Quote bằng 0 thì trả `denied`, không gọi host.
6. Quote lớn hơn 0 thì orchestrator, là bên duy nhất ghi tiền, gọi `durability.issue_refund` với **quote đầy đủ** (không tự trừ phần đã hoàn trước, để T13, T14 đúng) và truyền `crash_at` (CP3).
7. `InjectedCrash` được ghi vào trace rồi ném lại, không nuốt, để T12 thấy crash thật. Mọi nhánh trả về đều đi qua `finish()` nên `refund_effects` và `committed_audit_count` lấy từ ledger, trace luôn được ghi.

Số lần gọi model: 2 mỗi claim (`plan`, `draft`). Model chỉ soạn chữ, không quyết định số tiền.

Commit này không thêm hoặc sửa test.

## 4. Bằng chứng

Chạy trong `src/` với venv của project:

- `python -m pytest -q -m student -o addopts= -k orchestrator`: **62 passed** cho shape orchestrator.
- T11 (gọi lại cùng claim) và T12 (crash rồi resume) đều xanh trên orchestrator.
- `python -m pytest -q` (cổng host): 54 passed, không có dòng `failed`.

## 5. Công cụ AI đã dùng

Claude Code (mô hình Claude) được dùng để đọc đề, phân tích các TODO CP2/CP3, viết bản nháp `orchestrator.py`, giải thích luồng và soạn sơ đồ, script thuyết trình. Kết quả được kiểm bằng cách chạy ma trận student và cổng host ở mục 4.

## 6. Tự đánh giá

Thành viên tự điền trước khi nộp; chưa có xác nhận cá nhân.
