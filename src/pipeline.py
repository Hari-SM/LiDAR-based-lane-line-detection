import open3d as o3d

from thresholding import reflectivity_threshold
from region_of_interest import roi_filter
from visualization import visualize_pcd

def lane_line_detection(pcd, threshold=0.5, roi_min=(-20,-5,-2), roi_max=(20,5,2)):
    """
    This is a complete pipeline of this project. It uses the reflectivty property to identify
    the lane line, and using region of interest, it gives the final output.

    :param pcd: the input point cloud object
    :param threshold: the minimum reflectivity value required for the thresholding
    :param roi_min: a tuple(x, y, z), with minimum co-rodinate values of the region
    :param roi_max: a tuple(x, y, z), with maximum co-rodinate values of the region 
    :return roi_point_cloud: a pcd object with points only from the passed roi region above the threshold
    :return reflectivity_point_cloud: the point cloud file with points only above the thresholding reflectivity
    """
    reflectivity_point_cloud = reflectivity_threshold(pcd, threshold=threshold)
    roi_point_cloud = roi_filter(reflectivity_point_cloud, roi_min=roi_min, roi_max=roi_max)

    return roi_point_cloud, reflectivity_point_cloud

if __name__ == "__main__":
    ## Read point cloud file
    pcd = o3d.io.read_point_cloud("../data/KITTI_PCD/0000000200.pcd")

    ## Lane line detection based on reflectivity property
    roi_pcd, reflectivity_pcd = lane_line_detection(pcd, threshold=0.45, 
                                                    roi_min=(-20,-3,-2), roi_max=(20,3,0))
    
    ## Visualize the point cloud
    o3d.visualization.draw_geometries([pcd.paint_uniform_color((0.1, 0.1, 0.1)),
                                       roi_pcd])
    fig = visualize_pcd([pcd.paint_uniform_color((0.1,0.1,0.1)), roi_pcd], save="test")
    