
## スマホ利用による脳疲労をシミュレーションするアプリ
Qiita：[スマホ利用による脳疲労をPythonで視覚化してみた](https://qiita.com/shota-watanabe/items/a881c21150986dd3998f)

## 環境構築
### 前提
以下がインストールされていること。
- Python
- XQuartz

### 手順
1. ビルド
```
docker build -t brain-sim .
```

2. DockerからのGUI接続を許可
```
xhost +localhost
```

2. 起動
```
docker run -it --rm brain-sim
```

![Y34fIRFZ9Vkp8qcms2Fo1749952643-1749952649](https://github.com/user-attachments/assets/06528047-b34c-4cc5-862d-7b8bc7342686)

