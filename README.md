# Fine-tune PaddleX Models

Mục tiêu: hướng dẫn fine-tune bằng Kaggle và evaluate/export/infer ở local cho một số model PaddleX hay dùng.

Mục đích:
- fine-tune bằng Kaggle để tận dụng GPU free
- evaluate, export và infer ở local để bám sát môi trường thật

Cấu trúc:
- `kaggle/`: hướng dẫn hoặc file chạy trên Kaggle
- `export/`: file chạy ở local sau khi tải checkpoint từ Kaggle

## Hiện có

### 1. `PP-DocLayout_plus-L`

- Fine-tune: [kaggle/README_PP-Doclayout_plus_L](kaggle/README.md)
- Export/Evaluate/Infer: [export/README_PP-Doclayout_plus_L](export/README.md)

### 2. `PP-OCRv5_server_det`

- Fine-tune: [kaggle/README_PP-OCRv5_server_det.md](kaggle/README_PP-OCRv5_server_det.md)
- Export/Evaluate/Infer: [export/README_PP-OCRv5_server_det.md](export/README_PP-OCRv5_server_det.md)

## Ghi chú

- Luồng `PP-DocLayout_plus-L` đang bám theo dataset COCO object detection.
- Luồng `PP-OCRv5_server_det` dùng dataset text detection với `train.txt` và `val.txt`.
