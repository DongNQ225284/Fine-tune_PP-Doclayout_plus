# Export `PP-OCRv5_server_det`

## Export ở local

File: [export_PP-OCRv5_server_det.py](export_PP-OCRv5_server_det.py)

### 1. Clone PaddleX

```bash
git clone https://github.com/PaddlePaddle/PaddleX.git
cd PaddleX
```

### 2. Clone repo hướng dẫn

```bash
cd ..
git clone https://github.com/DongNQ225284/Fine-tune_PaddleOCR.git
cp Fine-tune_PaddleOCR/export/export_PP-OCRv5_server_det.py ./PaddleX/export/
```

### 3. Tạo môi trường sạch

Ví dụ với `conda`:

```bash
conda create -y -n ppocr_det_export python=3.10
conda activate ppocr_det_export
```

### 4. Cài dependency tối thiểu

Từ root repo `PaddleX`:

```bash
python -m pip install --upgrade pip wheel "setuptools<81"
python -m pip install -e .[base]
paddlex --install PaddleOCR -y
```

### 5. Đặt checkpoint vào đúng chỗ

Đặt 2 file tải từ Kaggle vào cùng một thư mục:

```text
weights/best_accuracy/
├── best_accuracy.pdparams
└── config.yaml
```

Lưu ý:

- `config.yaml` phải là file của đúng run train sinh ra `best_accuracy.pdparams`
- nếu `config.yaml` còn các path kiểu `/kaggle/working/...` thì nên đổi `save_dir` và `vdl_log_dir` sang path local writable để dễ evaluate/debug ở local

### 6. Chạy export

Nếu bạn đang đứng trong env sạch đã cài xong dependency:

```bash
python export/export_PP-OCRv5_server_det.py
```

Nếu muốn đổi vị trí weight hoặc output:

```bash
cd /path/to/PaddleX
WEIGHT_DIR=/path/to/weights/best_accuracy \
WEIGHT_PATH=/path/to/weights/best_accuracy/best_accuracy.pdparams \
TRAIN_CONFIG_PATH=/path/to/weights/best_accuracy/config.yaml \
EXPORT_DIR=/path/to/export_dir \
python export/export_PP-OCRv5_server_det.py
```

## Kết quả mong đợi sau export

```text
export_dir/
├── inference.json
├── inference.pdiparams
└── inference.yml
```

## Evaluate sau khi train

Điều kiện:

- có dataset local dạng text detection
- trong `dataset_dir` có `train.txt`, `val.txt`, và thư mục `images/`
- có file weight `weights/best_accuracy/best_accuracy.pdparams`

Ví dụ:

```bash
cd /path/to/PaddleX
conda run -n paddleX python3 main.py \
  -c paddlex/configs/modules/text_detection/PP-OCRv5_server_det.yaml \
  -o Global.mode=evaluate \
  -o Global.dataset_dir=/path/to/dataset_dir \
  -o Evaluate.weight_path=./weights/best_accuracy/best_accuracy.pdparams
```

Sau khi evaluate, PaddleX sẽ sinh `evaluate_result.json` với các metric như `precision`, `recall`, `hmean`.

## Infer demo sau khi export

Sau khi export xong và đã có thư mục `inference/`, có thể infer trực tiếp với ảnh local:

```bash
cd /path/to/PaddleX
conda run -n paddleX python3 main.py \
  -c paddlex/configs/modules/text_detection/PP-OCRv5_server_det.yaml \
  -o Global.mode=predict \
  -o Predict.model_dir=./inference \
  -o Predict.input=/path/to/demo.jpg
```

Lưu ý:

- `Predict.model_dir` phải trỏ vào thư mục export chứa `inference.json`, `inference.pdiparams`, `inference.yml`
- nếu chưa export mà chỉ muốn infer nhanh, có thể dùng luôn `output/.../best_accuracy/inference`
