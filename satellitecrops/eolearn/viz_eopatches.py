
### Data viz ###
import matplotlib.pyplot as plt
from rasterio.merge import merge

# Standard ML
import numpy as np

def create_bbox_gdf(bbox_list, info_list):
    '''Create GeoDataFrame from bboxes for being able to plot them'''
    geometry = [Polygon(bbox.get_polygon()) for bbox in bbox_list]

    idxs = [idx for idx, _ in enumerate(info_list)]
    idxs_x = [info["index_x"] for info in info_list]
    idxs_y = [info["index_y"] for info in info_list]

    bbox_gdf = gpd.GeoDataFrame({
        "index": idxs,
        "index_x": idxs_x,
        "index_y": idxs_y}, crs=32630, geometry=geometry)
    return bbox_gdf

def plotbboxes(bbox_list, info_list, title="BBoxes", fig_size = 10, bckgd_img=None, gdf_img=None, zone_covered=None):
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))
    ax.set_title(title, fontsize=0.2*fig_size)
    if gdf_img:
        gdf_img['geometry'].plot(ax=ax, alpha=0.1)
    if bckgd_img:
        if gdf_img:
            left, bottom, right, top = gdf_img['geometry'][0].bounds
            plt.imshow(np.moveaxis(bckgd_img,0,2), extent=(left, right, bottom, top), alpha=1)
        else:
            print("To plot background image (bckgd_img) the geodataframe of the image (gdf_image) should be provided")
    if zone_covered:
        zone_covered.plot(ax=ax, facecolor="w", edgecolor="b", alpha=0.8)

    bbox_gdf = create_bbox_gdf(bbox_list, info_list)
    bbox_gdf.plot(ax=ax, facecolor="w", edgecolor="r", alpha=0.5)
