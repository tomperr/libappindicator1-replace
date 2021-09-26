# libappindicator1-replace

## Introduction

On Debian 11 Bullseye, `libappindicator1` is deprecated. However, some packages still need it (like discord).
Using `libayatana-appindicator1` instead of the deprecated one solves problems.

## Requirements

Python 3 is needed to run script.

## Usage

```bash
python3 automate-change.py my_broken_package.deb
```

A new and fixed package prefixed by `modified_` will be created at your current working directory.

## Source

[How to modify and repack deb package](https://medium.com/@kasunmaduraeng/how-to-modify-and-repack-deb-package-436f8351af41)
