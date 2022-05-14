## 换脸流程
- 准备好需要换脸的目标人脸视频及目标人脸并做预处理
- 通过运行first-order-model中的crop.py得到ffmpeg命令用于裁剪视频
- 通过运行motion-cosegmentation中的swap.py将裁剪后的目标人脸视频以及目标人脸进行互换
- 通过第3步得到的ffmpeg命令中的人脸位置信息，将换脸之后的视频对齐回原视频

#### 人脸预处理流程
preprocess文件夹下

#### 过程
1. 安装环境依赖

```bash
# 根目录下
pip install -r requirements.txt
sudo apt-get update
sudo apt-get install ffmpeg

# first-order-model下安装face-aligment 用于裁剪人脸
git clone https://gitee.com/nosferatu/face-alignment.git
cd face-alignment
pip install -r requirements.txt
python setup.py install
```

2. 于first-order-model文件夹下，运行以下命令，得到包含需裁剪人脸位置以及对应视频片段的的ffmepg命令

```bash
python crop-video.py --inp path/to/target_video
```
以上命令的输出：

```bash
ffmpeg -i path/to/target_video -ss start_time -t  duration -filter:v "crop=left_top_x:left_top_y:right_bottom_x:right_bottom_y, scale=256:256" path/to/crop_video
```
- 参数：
      -ss为截取视频开始时间，duration为截取视频时长，crop为left_top_x:left_top_y:right_bottom_x:right_bottom_y, scale=256:256为最终缩放尺寸为256x256，

通过ffmpeg命令得到两种视频，一种为只有人脸部分的256x256视频，另一种为对应片段的完整视频

```bash
ffmpeg -i path/to/target_video -ss start_time -t  duration -filter:v "crop=left_top_x:left_top_y:right_bottom_x:right_bottom_y, scale=256:256" path/to/crop_video

ffmpeg -i path/to/target_video -ss start_time -t  duration path/to/target_video_divided
```

3. 对目标人脸做预处理

   裁剪到标准人脸，使人脸居中且占据图片主要面积

   ​                                 <img src="pics\justin.jpg" alt="justin" style="zoom:25%;" />         👉         <img src="pics\justin_crop.jpg" alt="justin_crop" style="zoom:25%;" />

4. 于motion-cosegmentation文件夹下运行以下命令，使用预处理之后的目标人脸，以及上一步裁剪好的目标视频进行换脸，得到换脸之后的视频

```bash
python part_swap.py  --config ./config/vox-256-sem-10segments.yaml  --target_video path/to/crop_video --source_image path/to/target_face --result_video path/to/result_video  --checkpoint ./checkpoints/vox-cpk.pth.tar --supervised --first_order_motion_model  --swap_index 1,2,3,4,5,6,10,11,12,13,17
```

经过多次实验对比，命令中的参数为是换脸结果主观上较好的搭配

- 参数：
      --swap_index 0:背景 1：除五官以外的脸部 2-5：眉毛 6：眼睛  7-9：耳朵  10：鼻子  11-13：嘴唇  14-15：颈部 16：肩部  17：头发  
  
  <img src="pics\index.png" alt="image-20210713110012765" style="zoom: 50%;" />

4. 通过ffmpeg将换好的人脸视频贴回原视频中

```bash
ffmpeg -i path/to/target_video_divided -i path/to/result_video -ss start_time -t  duration -filter_complex "[1:v]scale=left_top_x:left_top_y[v1];[0:v][v1]overlay=right_bottom_x:right_bottom_y"  -c:v libx264 path/to/final_video
```

#### 示例：

将目标人脸图片做预处理：使人脸能够占据图片的大部分面积，且居中

<img src="pics\target_face.jpg" alt="target_face" style="zoom:15%;" />

​                                                                                标准的目标人脸

```bash
# first-order-model
python crop-video.py --inp ../datasets/target_video.mp4
```

得到ffmepg命令

```bash
ffmpeg -i ../datasets/target_video.mp4 -ss 0.0 -t 9.533333333333333 -filter:v "crop=625:625:579:174, scale=256:256"  ../datasets/crop_video.mp4
```

得到两种视频：

```bash
ffmpeg -i ../datasets/target_video.mp4 -ss 0.0 -t 9.533333333333333 -filter:v "crop=625:625:579:174, scale=256:256"  ../datasets/crop_video.mp4
ffmpeg -i ../datasets/target_video.mp4 -ss 0.0 -t 9.533333333333333  ../datasets/target_video_divided.mp4
```

​                                                    <img src="pics\crop_video.png" alt="image-20210730103035180" style="zoom: 50%;" />              <img src="pics\target_video_divided.png" alt="image-20210730103107916" style="zoom: 67%;" />

进行换脸

```bash
# motion-cosegmentation
python part_swap.py  --config ./config/vox-256-sem-10segments.yaml  --target_video ../datasets/crop_video.mp4 --source_image ../datasets/target_face.jpg --result_video ../datasets/result_video.mp4  --checkpoint ./checkpoints/vox-cpk.pth.tar --supervised --first_order_motion_model  --swap_index 1,2,3,4,5,6,10,11,12,13,17
```

<img src="pics\result_video.png" alt="image-20210730103214103" style="zoom:50%;" />

将换好的脸贴回原视频

```
ffmpeg -i ../datasets/target_video_divided.mp4 -i ../datasets/result_video.mp4 -ss 0.0  -t  9.533333333333333 -filter_complex "[1:v]scale=625:625[v1];[0:v][v1]overlay=579:174"  -c:v libx264 ../datasets/final_video.mp4
```

<img src="pics\final_video.png" alt="image-20210730103214103" style="zoom:80%;" />


