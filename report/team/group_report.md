# Báo cáo nhóm — Lab 8 LogiX-VN, CP5

## 1. Thông tin nhóm

- Tên nhóm: nhóm LogiX-VN L3A (chưa có tên riêng trong `TEAM.md`)
- Thành viên: Ngô Hồng Hoàng, Nguyễn Quang Thành, Trần Việt Anh (xem `TEAM.md`)
- Commit code và bằng chứng được đánh giá: `14f96cf30576d8e6a3392a9e4723f919522c6a5f` (trùng ADR)

## 2. Mục tiêu và cách tiếp cận

Xử lý claim hoàn tiền theo order, policy và approval mà không lấy lời ticket làm dữ kiện quyết định tiền. So bốn shape trên cùng 14 claim, 5 seed và giá mô phỏng. Phân vai theo shape: Hoàng phụ trách workflow, Thành single, Việt Anh orchestrator; swarm là đối chứng có sẵn. Chạy ma trận public trước khi benchmark, sau đó dùng JSON sinh bởi harness để chọn kiến trúc.

## 3. Giải pháp

**Workflow:** đọc claim, kiểm order theo principal, tính quote từ order và policy, gọi `issue_refund` với *full quote*. Host tự kiểm approval và phần hoàn trước trên cùng order, rồi ghi ledger và audit. Không có model call trong kết quả benchmark.

**Single:** dùng vòng `run_react` tối đa 8 bước để chọn read tools `lookup_order`, `lookup_refund_history`, `compute_compensation`; MockLLM hỗ trợ bước quyết định, không được ghi refund. Host là writer duy nhất.

**Orchestrator:** tạo handoff qua `make_handoff` với facts rỗng và read-only tool allowlist. Investigator đọc order/policy và tính quote; orchestrator gọi host để ghi. `parent_secret`, `raw_headers`, ticket và PII không đi qua handoff. Trace ghi event an toàn (`claim`, `lookup_order`, `quote`, `decision`, `handoff`, `investigator`, kết quả ghi), tránh dữ liệu thô. `RunResult` và trace được đối chiếu với SQLite ledger.

## 4. Kết quả

Nguồn: `src/reports/benchmark.json`, lệnh `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`. Mỗi shape có 70 trial, SQLite mới cho từng trial. Cost là VND **mô phỏng**.

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success | Mean / p95 steps |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| workflow | 70/70 = 1,000 | 14/14 = 1,000 | 1,000–1,000 | 0 | 34,29 | 5,07 / 6 |
| single | 70/70 = 1,000 | 14/14 = 1,000 | 1,000–1,000 | 0 | 41,40 | 3,50 / 4 |
| orchestrator | 70/70 = 1,000 | 14/14 = 1,000 | 1,000–1,000 | 0 | 47,90 | 3,71 / 4 |
| swarm | 69/70 = 0,986 | 13/14 = 0,929 | 0,929–1,000 | 0,000816 | 49,57 | 2,80 / 3 |

Seed variance là phương sai tổng thể của năm pass rate theo seed. Cost/success chia **tổng cost tất cả trial**, kể cả fail, cho số trial pass. `pass^5` đếm claim đúng ở cả năm seed, nên C-002 sai một seed khiến swarm giảm từ 14/14 xuống 13/14. C-002/T02 ở seed 55: ticket báo trễ 5 ngày, order ghi 2; swarm trả `resolved` thay vì `denied` (`R-swarm-C-002-s55`). Crash suite: 20/20 (`src/reports/crash.json`). Ma trận student: 248 passed, 54 deselected. `student_drop/` chưa có, nên chưa thể tự kiểm hidden hay suy ra tỷ lệ hidden.

Quyết định chọn workflow: xem `decision_adr.md`. Phiếu R2 và đối chiếu workflow–swarm: xem `research_card.md`.

## 5. Khó khăn và cách xử lý

Ban đầu Git báo `detected dubious ownership` khi đọc repo. Các lệnh kiểm tra dùng `git -c safe.directory=D:/VinAI/Workflows/K5-L3B-DAY08-Workflows-FromWorkflowsToAgents`, không sửa cấu hình toàn cục. Swarm có một fail có chủ ý trên T02 seed 55; đối chiếu `src/reports/benchmark.json` với `src/lab8/shapes/swarm_reference.py` và order row cho thấy nhánh tin ticket. Không sửa benchmark JSON hoặc thước đo để che lỗi.

## 6. Tổng hợp đóng góp

Code shape có commit riêng cho Thành (`0e6dbd6`), Việt Anh (`6a6dbe8`) và workflow cùng bằng chứng CP5 ở `14f96cf` theo Git. Bảng đóng góp trong `TEAM.md` phân biệt test đã chạy với test từng người thực sự thêm; lịch sử hiện không ghi test mới trong các commit shape. Báo cáo cá nhân nằm ở `report/team/<MSSV>_<HoTen>.md`.

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất; latency là `unavailable`. Bộ public 14 claim không dự đoán chắc hidden 40 claim × 5 seed. Chỉ so shape hoàn chỉnh nên prompt và số call cũng thay đổi; không kết luận chênh lệch chỉ do topology. Sau khi có `student_drop/`, chạy self-check không nhãn để tìm `error`, trace hỏng và `leak_suspect`, rồi rà soát lại ADR; điểm hidden chính thức chỉ grader biết.

## 8. Tài liệu tham khảo

- `docs/metrics.md`, `docs/contracts.md`, `docs/architecture.md`, `src/README.md` của repo.
- Cemri và cộng sự, [*Why Do Multi-Agent LLM Systems Fail?*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html), NeurIPS 2025.
