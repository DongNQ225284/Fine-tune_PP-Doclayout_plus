# Fine-tune PP-Doclayout_plus_L in Kaggle 

## Cần import gì vào Kaggle?

Gắn 2 input vào notebook:

1. Dataset COCO object detection

Cấu trúc mong đợi:

```text
dataset/
├── images/
│   ├── train/
│   ├── valid/
│   └── test/          # optional
└── annotations/
    ├── instance_train.json
    ├── instance_valid.json
    └── instance_test.json    # optional
```

Trong đó:

```text
images/train/   <-> instance_train.json
images/valid/   <-> instance_valid.json
images/test/    <-> instance_test.json  # nếu có test
```

`file_name` trong COCO JSON nên trỏ đúng tới ảnh theo đường dẫn relative dưới `images/`, ví dụ:

```text
train/sample_00001.png
valid/sample_01001.png
test/sample_02001.png
```

Notebook sẽ bắt buộc có `train` và `valid`. Phần `test` là tùy chọn.

Ví dụ tối thiểu:

```text
dataset/
├── annotations/
│   ├── instance_train.json
│   └── instance_valid.json
└── images/
    ├── train/
    └── valid/
```

2. Pretrained weight `PP-DocLayout_plus-L_pretrained.pdparams`

## Cách chạy trên Kaggle

1. Upload notebook `fine-tune_PP-Doclayout_plus_L.ipynb` lên Kaggle
2. Gắn 2 input nói trên vào notebook
3. Mở cell `Configuration`
4. Chỉ sửa các biến sau cho đúng:

```python
DATASET_DIR
PRETRAIN_PATH
OUTPUT_DIR
NUM_CLASSES
DEVICE
EPOCHS
BATCH_SIZE
LEARNING_RATE
WARMUP_STEPS
EVAL_INTERVAL
LOG_INTERVAL
```

5. Bấm `Run All`

## Notebook sẽ tự làm gì?

- check dataset input có tồn tại không
- check pretrained weight có tồn tại không
- clone `PaddleX`
- cài môi trường và plugin `PaddleDetection`
- chạy `check_dataset`
- chạy `train`
- check output sau train
- zip output để tải về local

## File cần tải về sau khi train

Tối thiểu:

```text
output/<run_name>/best_model/best_model.pdparams
output/<run_name>/config.yaml
```

Khuyến nghị:

- tải cả file zip output mà notebook tạo ra
