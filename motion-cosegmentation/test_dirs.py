
import os
video_path = '/home/kpl/code/motion-cosegmentation/results'
videos = ['0003','0008','0010','0011','0015','0018','0023']
pics = ['0006','0010','0016','0034','0042','0047']
start_time = ['32.4','0.04','23.55689022355689','0.0','0.0','0.0','0.0',]
duration   = ['27.6','59.92','36.50316983650317','33.6','60.0','60.0','59.96666666666667']
for i in range(8):
    for j in range(6):
        tmp1 = 'output_'+ videos[i]+'_' +pics[j] + '.mp4'
        tmp2 = 'output_'+ videos[i]+'_' +pics[j] + '_cut.mp4'
        video_path_ = os.path.join(video_path, tmp1)
        out_path    = os.path.join(video_path,'cut', tmp2)
        print(f'ffmpeg -ss {start_time[i]} -i {video_path_} -vcodec copy -acodec copy -t {duration[i]}  {out_path}', end='\n\n')
