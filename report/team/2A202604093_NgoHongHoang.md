# Báo cáo cá nhân — Ngô Hồng Hoàng

## 1. Thông tin thành viên

- Họ tên: Ngô Hồng Hoàng
- MSSV: 2A202604093
- Danh tính Git: `HoangHongNgo <honghoangngo@gmail.com>`; GitHub của repo nhóm: `HoangHongNgo`

## 2. Phần việc phụ trách

Workflow, tích hợp benchmark và crash suite, tổng hợp quyết định kiến trúc CP5.

## 3. Đóng góp cụ thể

Commit `14f96cf30576d8e6a3392a9e4723f919522c6a5f` triển khai `src/lab8/shapes/workflow.py`, sinh benchmark và crash report. Workflow đọc claim qua view cho phép, kiểm quyền xem order theo principal, tính full quote từ order bằng code và gọi host `issue_refund`; không lấy số ngày trễ trong ticket làm căn cứ hoàn tiền. Các commit `0818203` và `660d975` ghi quyết định CP5, báo cáo và self-check với `student_drop/` cập nhật.

## 4. Bằng chứng

- Benchmark public: workflow đúng 70/70 trial, pass^5 14/14, cost/success 34,29 VND mô phỏng; run đối chiếu `R-workflow-C-002-s55`.
- Crash suite: 20/20. Cổng host: 54 passed; ma trận student toàn repo: 248 passed, 54 deselected.
- Self-check hidden không nhãn: workflow chạy 200/200 trial, không `error`, không `leak_suspect`, trace hợp lệ (`src/reports/hidden_selfcheck.json`). Không thể tính pass rate hidden từ bộ này.
- Giới hạn đóng góp test: các commit trên chưa thêm hoặc sửa test riêng; việc chạy test không đáp ứng yêu cầu rubric về test do từng thành viên đóng góp.

## 5. Công cụ AI đã dùng

Codex hỗ trợ soạn, rà báo cáo CP5 và chạy lại self-check. Số liệu được đối chiếu với JSON do harness sinh, output pytest và crash suite; không tạo nhãn cho `student_drop/` hoặc sửa tay report JSON. Việc dùng AI lúc viết workflow trước các lượt này không được ghi nhận trong repo.

## 6. Tự đánh giá

Theo bằng chứng kỹ thuật, workflow đã hoàn thành: public 70/70, crash 20/20, self-check hidden không lỗi chạy hoặc dấu hiệu lộ canary. Workflow có chi phí mô phỏng thấp nhất trong ba shape đạt 70/70 public. Giới hạn còn lại là thiếu test mới hoặc sửa test trong commit cá nhân; điểm hidden chính thức và đánh giá chủ quan của thành viên không có trong repo.
