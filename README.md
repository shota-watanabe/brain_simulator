
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

![wbtlPzO4g927rBd0BVcD1749953716-1749953720](https://github.com/user-attachments/assets/f5b4e81e-7f95-469c-b993-70cc7d3fdfd9)

