import open3d as o3d
import numpy as np

def reflectivity_threshold(pcd, threshold=0.5):
    """
    
    """
    ## Get the points and colors data from pcd
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)

    ## Reflectiivty is encoded in the colors
    reflectivity = colors[:, 0]

    ## Create a mask to filter the data using threshold value
    mask_reflectivity = reflectivity > threshold

    ## Filtering out the points and colors using threshold
    filtered_points = points[mask_reflectivity]
    filtered_colors = colors[mask_reflectivity]

    ## Create a reflectivity point cloud object
    reflectivity_point_cloud = o3d.geometry.PointCloud()
    reflectivity_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
    reflectivity_point_cloud.colors = o3d.utility.Vector3dVector(filtered_colors)

    return reflectivity_point_cloud
    

if __name__ == "__main__":
    ## Read PCD file 
    pcd = o3d.io.read_point_cloud("../data/KITTI_PCD/0000000200.pcd")

    ## Apply threshold filter to the reflectivity
    reflectivity_point_cloud = reflectivity_threshold(pcd, threshold=0.45)

    ## Visualize the Point cloud
    o3d.visualization.draw_geometries([pcd.paint_uniform_color((0.1, 0.1, 0.1)), 
                                       reflectivity_point_cloud])
