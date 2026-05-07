# Export PP-Doclayout_plus_L



## Export ở local

File: [export_PP-Doclayout_plus_L.py](export_PP-Doclayout_plus_L.py)

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
cp -r Fine-tune_PP-Doclayout_plus/export ./PaddleX
rm -rf Fine-tune_PP-Doclayout_plus
```

### 3. Tạo môi trường sạch

Ví dụ với `conda`:

```bash
conda create -y -n pp_doclayout_export python=3.10
conda activate pp_doclayout_export
```

### 3. Cài dependency tối thiểu

File requirements:

- [requirements.txt](requirements.txt)

Từ root repo `PaddleX`:

```bash
python -m pip install --upgrade pip wheel "setuptools<81"
python -m pip install -r export/requirements.txt
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
python export/export_PP-Doclayout_plus_L.py
```

Nếu muốn đổi vị trí weight hoặc output:

```bash
cd /path/to/PaddleX
WEIGHT_DIR=/path/to/weights/best_model \
WEIGHT_PATH=/path/to/weights/best_model/best_model.pdparams \
TRAIN_CONFIG_PATH=/path/to/weights/best_model/config.yaml \
EXPORT_DIR=/path/to/export_dir \
python export/export_PP-Doclayout_plus_L.py
```

## Kết quả mong đợi sau export

```text
export_dir/
├── inference.json
├── inference.pdiparams
└── inference.yml
```
