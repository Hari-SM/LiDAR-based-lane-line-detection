import open3d as o3d
import numpy as np

from thresholding import reflectivity_threshold

def roi_filter(pcd, roi_min=(-20, -5, -2), roi_max=(20, 5, 2)):
    """
    This function returns a point cloud object with points only from the given region
    of interest of the passed point cloud file.

    :param pcd: input point cloud file
    :param roi_min: a tuple(x, y, z), with minimum co-rodinate values of the region
    :param roi_max: a tuple(x, y, z), with maximum co-ordinate values of the region
    :return roi_point_cloud: a pcd object with points only from the passed roi region 
    """
    ## Read the points and colors
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)

    ## ROI filter mask
    mask_roi = np.logical_and.reduce((
        points[:, 0] >= roi_min[0],
        points[:, 0] <= roi_max[0],
        points[:, 1] >= roi_min[1],
        points[:, 1] <= roi_max[1],
        points[:, 2] >= roi_min[2],
        points[:, 2] <= roi_max[2]
    ))

    ## Filtering points with mask
    filtered_points = points[mask_roi]
    filtered_colors = colors[mask_roi]

    ## Create a new pcd object with filtered points
    roi_point_cloud = o3d.geometry.PointCloud()
    roi_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
    roi_point_cloud.colors = o3d.utility.Vector3dVector(filtered_colors)

    return roi_point_cloud

if __name__ == "__main__":
    ## Read the point cloud file
    pcd = o3d.io.read_point_cloud("../data/KITTI_PCD/0000000200.pcd")

    ## Reflectivity threholding
    reflectivity_point_cloud = reflectivity_threshold(pcd, 0.45)

    ## Filtering the region of interest
    roi_point_cloud = roi_filter(reflectivity_point_cloud, roi_min=(0, -3, -2), roi_max=(20, 3, 0))

    ## Visualize the point cloud
    o3d.visualization.draw_geometries([pcd.paint_uniform_color((0.1, 0.1, 0.1)),
                                       reflectivity_point_cloud])
    o3d.visualization.draw_geometries([pcd.paint_uniform_color((0.1, 0.1, 0.1)),
                                       roi_point_cloud])