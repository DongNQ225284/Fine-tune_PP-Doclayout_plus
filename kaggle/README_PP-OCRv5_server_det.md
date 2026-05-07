# Fine-tune `PP-OCRv5_server_det` in Kaggle

## Cần import gì vào Kaggle?

Gắn 1 input dataset vào notebook:

```text
dataset_dir/
├── images/
├── train.txt
└── val.txt
```

Trong đó:

- `train.txt` và `val.txt` là annotation file của PaddleOCR text detection
- mỗi dòng có dạng:

```text
images/img_0.jpg\t[{"transcription":"TEXT","points":[[31,10],[310,140],[420,220],[310,170]]}]
```

Không bắt buộc gắn pretrained weight bằng Kaggle Input, vì PaddleX có thể tự tải từ official URL:

- `PP-OCRv5_server_det_pretrained.pdparams`

## Cách chạy trên Kaggle

Notebook mẫu trong repo:

- [fine-tune_PP-OCRv5_server_det.ipynb](fine-tune_PP-OCRv5_server_det.ipynb)

Các bước:

1. Tạo notebook mới trên Kaggle hoặc upload notebook mẫu này
2. Attach dataset text detection
3. Clone `PaddleX`
4. Checkout đúng commit bạn muốn dùng
5. Cài dependency và backend PaddleOCR
6. Chạy `check_dataset`
7. Chạy `train`

Ví dụ tối thiểu:

```bash
git clone https://github.com/PaddlePaddle/PaddleX.git
cd PaddleX
python -m pip install --upgrade pip wheel "setuptools<81"
python -m pip install -e .[base]
paddlex --install PaddleOCR -y
python main.py -c paddlex/configs/modules/text_detection/PP-OCRv5_server_det.yaml \
  -o Global.mode=check_dataset \
  -o Global.dataset_dir=/kaggle/input/your_dataset
python main.py -c paddlex/configs/modules/text_detection/PP-OCRv5_server_det.yaml \
  -o Global.mode=train \
  -o Global.dataset_dir=/kaggle/input/your_dataset \
  -o Global.output=/kaggle/working/output/ppocrv5_server_det \
  -o Global.device=gpu:0
```

## Nên chỉnh gì khi train?

Các tham số nên ưu tiên chỉnh:

- `Global.dataset_dir`
- `Global.output`
- `Global.device`
- `Train.epochs_iters`
- `Train.batch_size`
- `Train.learning_rate`
- `Train.eval_interval`
- `Train.save_interval`
- `Train.pretrain_weight_path` nếu muốn dùng local pretrained riêng

Ví dụ train thử 1 epoch:

```bash
python main.py -c paddlex/configs/modules/text_detection/PP-OCRv5_server_det.yaml \
  -o Global.mode=train \
  -o Global.dataset_dir=/kaggle/input/your_dataset \
  -o Global.output=/kaggle/working/output/ppocrv5_server_det \
  -o Global.device=gpu:0 \
  -o Train.epochs_iters=1 \
  -o Train.batch_size=4
```

## File cần tải về sau khi train

Tối thiểu:

```text
output/ppocrv5_server_det/
├── best_accuracy/
│   ├── best_accuracy.pdparams
│   └── inference/
└── config.yaml
```

Khuyến nghị:

- tải cả thư mục output của run train
- giữ lại `config.yaml` của đúng run train để trace lại hyperparameter

## Lưu ý

- `PP-OCRv5_server_det` là text detection, không dùng format COCO như `PP-DocLayout_plus-L`
- trước khi train thật, nên chạy `check_dataset` để bắt lỗi format `train.txt` hoặc `val.txt`
- nếu chỉ cần inference trong Kaggle, có thể dùng luôn `best_accuracy/inference`
