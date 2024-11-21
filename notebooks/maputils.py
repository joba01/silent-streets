import numpy as np
from PIL import Image
from pyproj import Proj, Transformer, transform

# from mpl_toolkits.basemap import Basemap
# import matplotlib.pyplot as plt
# # setup Lambert Conformal basemap.
# m = Basemap(width=12000000,height=9000000,projection='lcc',
#             resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)


# convert lon/lat to x/y in mercator projection
def lonlat_to_mercator(lon: float, lat: float) -> tuple[float, float]:
    # Convert longitude and latitude to radians
    lon_rad = np.radians(lon)
    lat_rad = np.radians(lat)

    # Mercator projection formula
    x = lon_rad
    y = np.log(np.tan(np.pi / 4 + lat_rad / 2))

    # Scale to image size
    x = (x + np.pi) / (2 * np.pi)
    y = (np.pi - y) / (2 * np.pi)

    return x, y


def project_point_within_bounds(
    lon: float, lat: float, bounds, width: int, height: int
) -> tuple[int, int]:
    x, y = lonlat_to_mercator(lon, lat)

    # Normalize x and y within the bounds
    x = (x - lonlat_to_mercator(bounds[0][1], bounds[0][0])[0]) / (
        lonlat_to_mercator(bounds[1][1], bounds[1][0])[0]
        - lonlat_to_mercator(bounds[0][1], bounds[0][0])[0]
    )
    y = (y - lonlat_to_mercator(bounds[1][1], bounds[1][0])[1]) / (
        lonlat_to_mercator(bounds[0][1], bounds[0][0])[1]
        - lonlat_to_mercator(bounds[1][1], bounds[1][0])[1]
    )

    # Scale to image size
    x *= width
    y *= height

    return (int(x), int(y))


P3857 = Proj(init="epsg:3857")
P4326 = Proj(init="epsg:4326")


def wgs84_to_web_mercator(coords, bounds, width, height):

    # Convert the coordinates from WGS84 to Web Mercator
    # x_mercator, y_mercator = transform(P4326, P3857, coords[1], coords[0])
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    x_mercator, y_mercator = transformer.transform(coords[0], coords[1])
    # print ("x,y", x_mercator, y_mercator)
    # Convert the bounds from WGS84 to Web Mercator
    x_min, y_min = transformer.transform(bounds[0][1], bounds[0][0])
    # print("x_min, y_min", x_min, y_min)
    x_max, y_max = transformer.transform(bounds[1][1], bounds[1][0])
    # print("x_max, y_max", x_max, y_max)
    # Normalize the coordinates within the bounds
    x_normalized = (x_mercator - x_min) / (x_max - x_min)
    y_normalized = (y_mercator - y_min) / (y_max - y_min)
    # print(x_normalized, y_normalized)
    # Scale to image size
    x_image = x_normalized * width
    y_image = (1 - y_normalized) * height  # Invert y-axis for image coordinates

    return x_image, y_image

def wgs84_to_web_mercator_array(xx:np.ndarray, yy:np.ndarray, bounds, width, height):
    # Convert the coordinates from WGS84 to Web Mercator
    # x_mercator, y_mercator = transform(P4326, P3857, coords[1], coords[0])
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    x_mercator, y_mercator = transformer.transform(xx, yy)
    # print ("x,y", x_mercator, y_mercator)
    # Convert the bounds from WGS84 to Web Mercator
    x_min, y_min = transformer.transform(bounds[0][1], bounds[0][0])
    # print("x_min, y_min", x_min, y_min)
    x_max, y_max = transformer.transform(bounds[1][1], bounds[1][0])
    # print("x_max, y_max", x_max, y_max)
    # Normalize the coordinates within the bounds
    x_normalized = (x_mercator - x_min) / (x_max - x_min)
    y_normalized = (y_mercator - y_min) / (y_max - y_min)
    # print(x_normalized, y_normalized)
    # Scale to image size
    x_image = x_normalized * width
    y_image = (1 - y_normalized) * height  # Invert y-axis for image coordinates

    x_image = x_image.round().astype(int)
    y_image = y_image.round().astype(int)
    
    return x_image, y_image



def draw_center_point(
    image: Image.Image, point_mercator: tuple[float, float], size=1
) -> Image.Image:
    width, height = image.size
    x, y = point_mercator
    x = round(x)
    y = round(y)

    # print(x, y)
    size_half = size // 2
    lower_bound = -size_half
    upper_bound = size_half + 1

    for dx in range(lower_bound, upper_bound):
        for dy in range(lower_bound, upper_bound):
            px = int(x) + dx
            py = int(y) + dy
            if 0 <= px < width and 0 <= py < height:
                image.putpixel((px, py), (255, 0, 0))  # Red color for the center point

    return image
