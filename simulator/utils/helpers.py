import math
import typing
import os
import importlib
import primitives
from collision import Vector, Poly

ShapeType = typing.Union[primitives.Rectangle, primitives.Ellipse]

def hex_to_rgb(hex_color):
  """Transforms a color from hecadecimal string (e.g. #FF0000)
  To rgba, with values from 0.0 to 255.0, which is pyglet standard.
  """
  r = hex_color[1:3]
  g = hex_color[3:5]
  b = hex_color[5:]
  return (int(r, 16) / 255, int(g, 16) / 255, int(b, 16) / 255, 0.0)

def parse_style(style):
  s = {}
  items = style.split(';')
  for item in items:
    if item == "":
      continue
    elif '=' not in item:
      s[item] = True
      continue
    [key, value] = item.split('=')
    s[key] = value
  return s

def get_rel_points(center, points):
  return list(map(lambda x: Vector(x[0] - center[0], x[1] - center[1]), points))

def tuple2vector(x):
  return Vector(x[0], x[1])
  
def rotate_around_point(xy, radians, origin=(0, 0)):
    """Rotate a point around a given point.
    
    I call this the "high performance" version since we're caching some
    values that are needed >1 time. It's less readable than the previous
    function but it's faster.
    From: https://gist.github.com/LyleScott/e36e08bfb23b1f87af68c9051f985302
    """
    x, y = xy
    offset_x, offset_y = origin
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = math.cos(radians)
    sin_rad = math.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y

    return qx, qy


def collision_from_points(shape: ShapeType, center: typing.Tuple[int, int]) -> Poly:
    points = shape._get_points()
    col_points = list(map(lambda x: Vector(x[0] - center[0], x[1] - center[1]), points))
    return Poly(tuple2vector(center), col_points)


def list_folder(path: str) -> typing.Dict:
    available = {}
    for component in os.listdir(path):
        file_name, extension = os.path.splitext(component)
        if not extension == '.py':
            continue
        if file_name.startswith('__') and file_name.endswith('__'):
            continue
        module = importlib.import_module(f'{path[2:]}.{file_name}')
        available[file_name] = module
    return available
