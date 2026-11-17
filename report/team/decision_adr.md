# Decision record — CP5

- Shape chọn: workflow
- Commit hash: 14f96cf30576d8e6a3392a9e4723f919522c6a5f
- Run id dẫn chứng: R-workflow-C-001-s11; đối chứng lỗi R-swarm-C-002-s55 (src/reports/benchmark.json)
- Pass rate / pass^5 / seed min-max / variance: 70/70 = 1,000 / 14/14 = 1,000 / 1,000–1,000 / 0,000000 trên public
- Cost per success (mô phỏng, VND): 34,285714 (tổng 2.400/70 trial pass)
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 0/70 trial public bị đánh dấu leak hoặc bypass theo evaluator; chưa có điểm hidden

## Vì sao shape này

Benchmark dùng cùng 14 claim, seed 11,22,33,44,55, MockLLM, `as_of`, tool, giá và evaluator. Ba shape nhóm viết đều đạt 70/70 và pass^5 14/14; workflow có cost/success thấp nhất: 34,29 VND, so với single 41,40 và orchestrator 47,90. Swarm đạt 69/70, pass^5 13/14, variance 0,000816 và cost/success 49,57. Workflow lấy `delay_days` từ order đã kiểm principal, quote bằng policy trong code, rồi để host kiểm approval, cap và ledger. Nó không phụ thuộc vào diễn giải ticket để chọn tiền.

## Có đáng đổi lấy multi-agent không

Trên public, orchestrator không tăng pass rate hay pass^5 so với workflow nhưng tốn thêm 13,62 VND cho mỗi trial đúng (khoảng 39,7%). Swarm còn có một lỗi ở T02 seed 55: ticket nói trễ 5 ngày, order chỉ trễ 2 ngày; nhánh `REFERENCE_WEAKNESS` tin ticket, đề xuất hoàn và trả `resolved` thay vì `denied`. Đây là lỗi kiểm chứng nguồn dữ liệu; host không thay được việc đối chiếu delay của shape. Quyết định sẽ đổi nếu hidden 200 trial cho thấy workflow dưới ngưỡng 0,75 hoặc thua shape khác ở pass rate/pass^5, trong khi shape đó vẫn đạt 20/20 crash, không leak/bypass và chênh cost/success hợp lý. Cần đánh giá lại trên claim mới trước khi đảo quyết định.

## Trace và bằng chứng

Workflow ghi `claim` với id và cờ found, `lookup_order` với visible/reason, `quote`, `issue_refund` với proposal, `host_result` và `decision`. Không ghi ticket, `parent_secret`, raw header, số điện thoại, địa chỉ, tên hàng hay ghi chú nội bộ. Handoff của orchestrator đi qua allowlist `make_handoff`, chỉ cho investigator read-only tools; trace ghi handoff đã sanitize. Contract trace v1 yêu cầu file mới, `run_id` khớp và `events` là list. Scanner kiểm file trace và mọi file cùng prefix `<run_id>*` trong cùng thư mục; trace nằm ngoài vùng quét phải được đưa vào hợp đồng hoặc bị xem là không kiểm chứng được, không thể tuyên bố an toàn chỉ từ kết quả JSON.

## Giới hạn

MockLLM và giá token là mô phỏng, không suy rộng sang model sản xuất; latency là `unavailable`. Public có 14 claim nên 70/70 không chứng minh hidden sẽ đạt 0,75. `student_drop/` chưa được phát tại thời điểm tạo quyết định; chưa có pass rate hidden chính thức.
