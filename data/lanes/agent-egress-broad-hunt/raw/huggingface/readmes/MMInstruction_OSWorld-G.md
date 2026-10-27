---
dataset_info:
  features:
  - name: id
    dtype: string
  - name: image_path
    dtype: string
  - name: image_size
    sequence: int64
  - name: instruction
    dtype: string
  - name: box_type
    dtype: string
  - name: box_coordinates
    sequence: float64
  - name: GUI_types
    sequence: string
  - name: image
    dtype: image
  - name: mimo_bbox
    sequence: float64
  splits:
  - name: test
    num_bytes: 251321485.0
    num_examples: 510
  download_size: 127374329
  dataset_size: 251321485.0
configs:
- config_name: default
  data_files:
  - split: test
    path: data/test-*
---
