# Cyantize

File safety sanitizer.

Purpose:

* File Type Verification
* AntiVirus / Malware File Verification
* File Dearmament and Reconstruction

## Setup

```commandline
sudo apt install -y pre-commit
pre-commit install

git lfs fetch --all
```

## Test

```commandline
pip3 install -e .
pytest test
```

resources are taken from https://file-examples.com/
