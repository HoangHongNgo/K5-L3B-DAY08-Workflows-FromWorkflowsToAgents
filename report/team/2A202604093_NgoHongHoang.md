# Báo cáo cá nhân — Ngô Hồng Hoàng

## 1. Thông tin thành viên

- Họ tên: Ngô Hồng Hoàng
- MSSV: 2A202604093
- Email/GitHub: chưa xác nhận trong `TEAM.md`

## 2. Phần việc phụ trách

Workflow, tổng hợp benchmark CP5 và quyết định kiến trúc.

## 3. Đóng góp cụ thể

Workflow trong `src/lab8/shapes/workflow.py` đọc order theo principal, tính quote bằng code và gọi host `issue_refund` với full quote; code cùng benchmark/crash được ghi ở commit `14f96cf30576d8e6a3392a9e4723f919522c6a5f`. Lịch sử commit này chưa có test riêng được thêm hoặc sửa; cần bổ sung bằng chứng test cá nhân trước khi nộp nếu rubric yêu cầu.

## 4. Bằng chứng

`src/reports/benchmark.json`: workflow 70/70, pass^5 14/14, cost/success 34,29 VND mô phỏng; run `R-workflow-C-002-s55`. `src/reports/crash.json`: 20/20. Ma trận student chạy 248 passed, 54 deselected.

## 5. Công cụ AI đã dùng

Codex hỗ trợ tổng hợp báo cáo CP5 trong lượt làm này; số liệu được đối chiếu với JSON do harness sinh và lệnh test. Công cụ dùng khi viết workflow trước lượt này chưa được xác nhận.

## 6. Tự đánh giá

Thành viên tự điền trước khi nộp; chưa có xác nhận cá nhân.
