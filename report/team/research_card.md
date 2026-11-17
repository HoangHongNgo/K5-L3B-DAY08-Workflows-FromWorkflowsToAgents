# Research card — CP5

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R2 |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng | Cemri và cộng sự, *Why Do Multi-Agent LLM Systems Fail?*, NeurIPS 2025, https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html ; nghiên cứu thực nghiệm và taxonomy. |
| CLAIM | Một kết luận gốc của nguồn | MAST phân loại 14 failure mode của hệ multi-agent thành 3 nhóm: thiết kế hệ thống, lệch phối hợp giữa agent, và kiểm chứng/kết thúc tác vụ. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận | Taxonomy rút từ dữ liệu và các framework mà bài báo khảo sát; không phải tỷ lệ lỗi dự đoán cho LogiX-VN hoặc MockLLM. |
| HYPOTHESIS | Nếu đổi shape A→B, metric X đổi thế nào | Với T02 seed 55, đổi workflow → swarm sẽ tạo một lỗi do tin ticket; trên 14 claim × 5 seed, dự đoán pass rate giảm từ 1 xuống 69/70, pass^5 từ 1 xuống 13/14 và variance tăng khỏi 0. |
| METHOD | Biến giữ cố định và biến thay đổi | Lệnh benchmark bên dưới giữ corpus, 5 seed, world, MockLLM, as_of, giá, evaluator và SQLite mới mỗi trial; biến so sánh là shape workflow hay swarm. |
| FAILURE / METRIC | Lỗi dự kiến và phép đo | C-002 seed 55 trả resolved thay vì denied; đo pass rate, pass^5, seed variance, cost/success và đọc trial reason cùng run id. |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Run id / file report: `R-workflow-C-002-s55`, `R-swarm-C-002-s55`; `src/reports/benchmark.json`.
- Kết quả so với hypothesis: đúng trên public. Workflow 70/70, pass^5 14/14, variance 0; swarm 69/70, pass^5 13/14, variance 0,0008163265. Trial sai duy nhất là C-002 seed 55, `status resolved != denied`. Cost/success tương ứng 34,29 và 49,57 VND mô phỏng.
- Giới hạn: đây là đối chiếu theo shape hoàn chỉnh, nên prompt, số model call và đường đọc tool cũng khác nhau; chưa cô lập riêng topology hoặc thao tác kiểm chứng. MAST chỉ giúp đặt tên loại lỗi, không chứng minh nguyên nhân thống kê. MockLLM không phải model sản xuất; latency là `unavailable`.
