import cv2
import open3d as o3d
from tqdm import tqdm
from glob import glob

from pipeline import lane_line_detection
from visualization import visualize_pcd

## Creating a video writer object
output_handle = cv2.VideoWriter("../output/lane_line_detection.avi", 
                                cv2.VideoWriter_fourcc(*'DIVX'), 10, (2400, 1599))

## Selecting the start and stop index
start_index = 350
stop_index = 400

## Creating a progress bar
pbar = tqdm(total=(stop_index-start_index), position=0, leave=True)

## Reading all point cloud files
point_cloud_files = sorted(glob("../data/KITTI_PCD/*.pcd"))
all_files = [o3d.io.read_point_cloud(point_cloud_files[i]) for i in range(start_index, stop_index)]

## Processing the land line detection and write a video
for i in range(len(all_files)):
    roi_pcd, reflectivity_pcd = lane_line_detection(all_files[i],
                                                    threshold=0.45,
                                                    roi_min=(-20, -3, -2),
                                                    roi_max=(20, 3, 0))
    fig = visualize_pcd([all_files[i].paint_uniform_color((0.1,0.1,0.1)), roi_pcd], 
                        show=False, save=str(start_index+i))
    output_handle.write(cv2.imread("../output/"+str(start_index+i)+".jpg"))
    pbar.update(1)

output_handle.release()


