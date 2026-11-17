# Báo cáo cá nhân — Nguyễn Quang Thành

## 1. Thông tin thành viên

- Họ tên: Nguyễn Quang Thành
- MSSV: 2A202604085
- Danh tính Git ghi ở commit: `Nguyen Quang Thanh <thanhquang32@gmail.com>`; GitHub cá nhân không có bằng chứng trong repo

## 2. Phần việc phụ trách

Single Agent shape với vòng ReAct tối đa tám bước, tool chỉ đọc và ranh giới ghi refund qua host.

## 3. Đóng góp cụ thể

Commit `0e6dbd6588a2cc303a1e83c193e9e4a1533d435a` triển khai `src/lab8/shapes/single.py`. Shape dùng `get_claim_view` và các tool đọc `lookup_order`, `lookup_refund_history`, `compute_compensation`; MockLLM được gọi ở bước quyết định nhưng lựa chọn tool do code điều khiển. Code lấy full quote từ order rồi gọi host `issue_refund`, chuyển `crash_at` để kiểm thử crash và idempotency. Commit này chưa thêm hoặc sửa test riêng.

## 4. Bằng chứng

- Benchmark public: single 70/70, pass^5 14/14, cost/success 41,40 VND mô phỏng; run `R-single-C-002-s55`.
- Cổng host: 54 passed; ma trận student toàn repo: 248 passed, 54 deselected; crash suite toàn repo: 20/20.
- Self-check hidden không nhãn: 200/200 trial chạy không lỗi, trace hợp lệ, không `leak_suspect`. Bộ này không thể cho pass rate hidden.

## 5. Công cụ AI đã dùng

Codex được dùng khi làm bài và tổng hợp báo cáo CP5; số liệu được kiểm bằng benchmark JSON, ma trận student và self-check hidden.

## 6. Tự đánh giá

Bài lab rất sát với lý thuyết, cá nhân và nhóm đã hoàn thành tốt.
