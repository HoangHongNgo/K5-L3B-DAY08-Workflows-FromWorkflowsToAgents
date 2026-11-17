# Team

## Thông tin nhóm

- Tên nhóm: LogiX-VN L3A (tên mô tả; nhóm chưa đặt tên riêng)
- Lớp: L3A
- Repo đang làm việc: `K5-L3B-DAY08-Workflows-FromWorkflowsToAgents`
- URL repo: https://github.com/HoangHongNgo/K5-L3B-DAY08-Workflows-FromWorkflowsToAgents.git
- Nhánh đang làm việc: `main`
- Commit code và benchmark được đánh giá: `14f96cf30576d8e6a3392a9e4723f919522c6a5f` (commit báo cáo CP5 có thể đến sau)

## Thành viên

| STT | Họ tên             | MSSV        | Email | GitHub | Vai trò      |
| --: | ------------------ | ----------- | ----- | ------ | ------------ |
|   1 | Ngô Hồng Hoàng     | 2A202604093 |       |        | Workflow     |
|   2 | Nguyễn Quang Thành | 2A202604085 |       |        | Single Agent |
|   3 | Trần Việt Anh      | 2A202604029 |       |        | Orchestrator |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người              | Vai                      | Commit                                 | Test đã thêm hoặc sửa                                                                           |
| ------------------ | ------------------------ | -------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Ngô Hồng Hoàng     | Workflow và tổng hợp CP5 | `14f96cf` (workflow, benchmark, crash) | Đã chạy `test_public_matrix.py` cho workflow; lịch sử chưa có test riêng được thêm/sửa          |
| Nguyễn Quang Thành | Single Agent             | `0e6dbd6` (single shape)               | Đã chạy `test_public_matrix.py` cho single; commit shape chưa có test riêng được thêm/sửa       |
| Trần Việt Anh      | Orchestrator             | `6a6dbe8` (orchestrator shape)         | Đã chạy `test_public_matrix.py` cho orchestrator; commit shape chưa có test riêng được thêm/sửa |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## MSSV_HoTen

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-

## 2A202604029_TranVietAnh

### Phần việc phụ trách

- Shape C `orchestrator`: CP2 (viết luồng orchestrator + investigator chỉ đọc trong `src/lab8/shapes/orchestrator.py`) và CP3 (handoff không mang secret, ghi tiền an toàn khi gọi lại và khi crash).

### Đóng góp cụ thể

- Commit `6a6dbe8` ("CP2, CP3 orchestrator"), chỉ sửa `src/lab8/shapes/orchestrator.py`.
- Đọc claim qua `get_claim_view` (không có `parent_secret`, `raw_headers`); thiếu `order_id` trả `needs_info`, claim không tồn tại trả `failed`.
- Dựng handoff bằng `make_handoff` với `facts = {}` và ba tool chỉ đọc; trace ghi handoff đã sanitize, không ghi parent context.
- Đơn không thấy hoặc không thuộc principal trả `escalated`; quote bằng 0 trả `denied` và không gọi host.
- Quote lấy từ `compute_compensation` trên order trong DB, không dùng số ngày trong ticket. Quote lớn hơn 0 thì gọi `durability.issue_refund` với quote đầy đủ và truyền `crash_at`; `InjectedCrash` được ghi trace rồi ném lại.
- Báo cáo cá nhân: `report/team/2A202604029_TranVietAnh.md`.

### Bằng chứng

- `python -m pytest -q -m student -o addopts= -k orchestrator`: 62 passed, gồm T11 (gọi lại) và T12 (crash/resume).
- `python -m pytest -q` (cổng host): 54 passed, không có `failed`.
- Chưa thêm hoặc sửa test riêng trong commit này.
