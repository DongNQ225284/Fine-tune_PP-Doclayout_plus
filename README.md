# Fine-tune & Export `PP-DocLayout_plus-L`

Mục tiêu: Trình bày quy trình fine-tune `PP-DocLayout_plus-L` bằng Kaggle, sau đó export model tại máy local

Mục đích:
- Fine-tune bằng Kaggle để tận dụng nguồn GPU free
- Export model tại local để bảm bảo độ tương thích với môi trường local

Cấu trúc:
- `kaggle/`: file chạy trên Kaggle
- `export/`: file chạy ở local sau khi tải checkpoint từ Kaggle

Hướng dẫn:
- [Fine-tune](kaggle/README.md)
- [Export](export/README.md)

