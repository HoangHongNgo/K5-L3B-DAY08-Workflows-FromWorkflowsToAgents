# Báo cáo cá nhân — Trần Việt Anh

## 1. Thông tin thành viên

- Họ tên: Trần Việt Anh
- MSSV: 2A202604029
- Danh tính Git: `Vietzanh <154943665+Vietzanh@users.noreply.github.com>`; tài khoản GitHub theo địa chỉ noreply: `Vietzanh`

## 2. Phần việc phụ trách

Orchestrator, investigator chỉ đọc và handoff được lọc theo allowlist.

## 3. Đóng góp cụ thể

Commit `6a6dbe82d2d1bf13980fba100a2e285b47263172` triển khai `src/lab8/shapes/orchestrator.py`. Orchestrator tạo handoff bằng `make_handoff`, chỉ cấp tool đọc cho investigator và ghi trace của handoff đã lọc. Investigator đọc order và tính quote; chỉ orchestrator gọi host `issue_refund` với full quote. Shape chuyển `crash_at` cho host và để `InjectedCrash` lan ra sau khi ghi trace crash.

## 4. Bằng chứng

- Benchmark public: orchestrator đúng 70/70 trial, pass^5 14/14, cost/success 47,90 VND mô phỏng; run đối chiếu `R-orchestrator-C-002-s55`.
- Cổng host: 54 passed; ma trận student toàn repo: 248 passed, 54 deselected; crash suite toàn repo: 20/20.
- Self-check hidden không nhãn: orchestrator chạy 200/200 trial, không `error`, không `leak_suspect`, trace hợp lệ. Không thể tính pass rate hidden từ bộ này.
- Giới hạn đóng góp test: commit triển khai orchestrator chưa thêm hoặc sửa test riêng; chạy test có sẵn không đáp ứng yêu cầu test cá nhân của rubric.

## 5. Công cụ AI đã dùng

Codex hỗ trợ tổng hợp báo cáo cá nhân này từ commit, benchmark JSON và output test. Repo không ghi nhận công cụ AI đã dùng lúc triển khai orchestrator, nên không gán thêm công cụ cho thành viên. Kết quả được đối chiếu bằng pytest, benchmark và self-check, không sửa tay JSON.

## 6. Tự đánh giá

Theo bằng chứng kỹ thuật, orchestrator đáp ứng contract public và giữ handoff chỉ đọc: public 70/70, self-check hidden không lỗi chạy hoặc dấu hiệu lộ canary. Cost/success 47,90 VND mô phỏng cao hơn workflow và single khi public cùng đạt 70/70, nên chưa có bằng chứng để chọn orchestrator cho tác vụ này. Giới hạn còn lại là thiếu test mới hoặc sửa test trong commit cá nhân; điểm hidden chính thức và đánh giá chủ quan của thành viên không có trong repo.
