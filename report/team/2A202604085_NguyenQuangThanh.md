# Báo cáo cá nhân — Nguyễn Quang Thành

## 1. Thông tin thành viên

- Họ tên: Nguyễn Quang Thành
- MSSV: 2A202604085
- Danh tính Git: `Nguyen Quang Thanh <thanhquang32@gmail.com>`; GitHub cá nhân không có bằng chứng trong repo

## 2. Phần việc phụ trách

Single Agent shape với vòng ReAct tối đa tám bước, tool chỉ đọc và ranh giới ghi refund qua host.

## 3. Đóng góp cụ thể

Commit `0e6dbd6588a2cc303a1e83c193e9e4a1533d435a` triển khai `src/lab8/shapes/single.py`. Shape dùng `get_claim_view` và các tool đọc `lookup_order`, `lookup_refund_history`, `compute_compensation`; MockLLM được gọi ở bước quyết định nhưng lựa chọn tool do code điều khiển, không quyết số tiền hoặc ghi refund. Sau vòng ReAct, code lấy full quote từ order và gọi `issue_refund`; `crash_at` được chuyển tới host để kiểm thử crash và idempotency.

## 4. Bằng chứng

- Benchmark public: single đúng 70/70 trial, pass^5 14/14, cost/success 41,40 VND mô phỏng; run đối chiếu `R-single-C-002-s55`.
- Cổng host: 54 passed; ma trận student toàn repo: 248 passed, 54 deselected; crash suite toàn repo: 20/20.
- Self-check hidden không nhãn: single chạy 200/200 trial, không `error`, không `leak_suspect`, trace hợp lệ. Không thể tính pass rate hidden từ bộ này.
- Giới hạn đóng góp test: commit triển khai single chưa thêm hoặc sửa test riêng; chạy test có sẵn không thay thế yêu cầu này trong rubric.

## 5. Công cụ AI đã dùng

Codex hỗ trợ tổng hợp báo cáo cá nhân này từ commit, benchmark JSON và output test. Repo không ghi nhận công cụ AI đã dùng lúc triển khai single, nên không gán thêm công cụ cho thành viên. Các kết quả được kiểm bằng pytest và benchmark, không sửa tay JSON.

## 6. Tự đánh giá

Theo bằng chứng kỹ thuật, single đáp ứng contract public và ranh giới đọc/ghi: public 70/70, self-check hidden không lỗi chạy hoặc dấu hiệu lộ canary. Chi phí mô phỏng cao hơn workflow (41,40 so với 34,29 VND mỗi trial đúng), nên kết quả hiện có chưa cho thấy lợi ích để chọn single. Giới hạn còn lại là thiếu test mới hoặc sửa test trong commit cá nhân; điểm hidden chính thức và đánh giá chủ quan của thành viên không có trong repo.
