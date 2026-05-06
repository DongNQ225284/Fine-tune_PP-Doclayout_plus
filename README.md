# Kaggle Run All Guide for `PP-DocLayout_plus-L`

Cấu trúc:

- `kaggle/train/`: file chạy trên Kaggle
- `kaggle/local/`: file chạy ở local sau khi tải checkpoint từ Kaggle


Notebook chính:

- [fine-tune_PP-Doclayout_plus_L.ipynb](/home/nqd/workspace/project/PaddleX/kaggle/train/fine-tune_PP-Doclayout_plus_L.ipynb)

## Cần import gì vào Kaggle?

Gắn 2 input vào notebook:

1. Dataset COCO object detection

Cấu trúc mong đợi:

```text
dataset/
├── annotations/
│   ├── instance_train.json
│   └── instance_val.json
└── images/
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

## Notebook sẽ tự làm gì

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

## Export ở local

File: [export_PP-Doclayout_plus_L.py](/home/nqd/workspace/project/PaddleX/kaggle/local/export_PP-Doclayout_plus_L.py)

### 1. Clone PaddleX

```bash
git clone https://github.com/PaddlePaddle/PaddleX.git
cd PaddleX
git checkout 0acbb30720b71566717d12540381187b1fff0948
```

### 2. Clone Fine-tune PP-Doclayout+

```bash
cd ..
git clone https://github.com/DongNQ225284/Fine-tune_PP-Doclayout_plus

#move files from Fine-tune_PP-Doclayout_plus to PaddleX
mv Fine-tune_PP-Doclayout_plus/* ./PaddleX
```

### 3. Tạo môi trường sạch

Ví dụ với `conda`:

```bash
conda create -y -n pp_doclayout_export python=3.10
conda activate pp_doclayout_export
```

### 3. Cài dependency tối thiểu

File requirements:

- [requirements.txt](/home/nqd/workspace/project/PaddleX/requirements.txt)

Từ root repo `PaddleX`:

```bash
python -m pip install --upgrade pip wheel "setuptools<81"
python -m pip install -r requirements.txt
paddlex --install PaddleDetection -y
```

### 4. Đặt checkpoint vào đúng chỗ

Đặt 2 file tải từ Kaggle vào cùng một thư mục:

```text
weights/best_model/
├── best_model.pdparams
└── config.yaml
```

Lưu ý:

- `config.yaml` phải là file của đúng run train sinh ra `best_model.pdparams`
- nếu `config.yaml` còn các path kiểu `/kaggle/working/...` thì sửa sang path local writable trước khi export

### 5. Chạy export

Nếu bạn đang đứng trong env sạch đã cài xong dependency:

```bash
cd /path/to/PaddleX
python kaggle/local/export_PP-Doclayout_plus_L.py
```

Nếu muốn đổi vị trí weight hoặc output:

```bash
cd /path/to/PaddleX
WEIGHT_DIR=/path/to/weights/best_model \
WEIGHT_PATH=/path/to/weights/best_model/best_model.pdparams \
TRAIN_CONFIG_PATH=/path/to/weights/best_model/config.yaml \
EXPORT_DIR=/path/to/export_dir \
python kaggle/local/export_PP-Doclayout_plus_L.py
```

## Kết quả mong đợi sau export

```text
export_dir/
├── inference.json
├── inference.pdiparams
└── inference.yml
```
