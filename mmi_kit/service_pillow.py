import numpy as np
from PIL import Image, ImageDraw

from mmi_kit.service_pixelarray import PixelarrayService


class PillowService(object):

    @staticmethod
    def overlay_with_point(rgb_img, point, color="blue", radius=5):
        assert (len(point) <= 3)
        draw = ImageDraw.Draw(rgb_img)
        draw.ellipse((point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius), fill=color)

    @staticmethod
    def overlay_with_line(rgb_img, points, color="blue", width=1, make_loop=False):
        assert (isinstance(points, list))
        draw = ImageDraw.Draw(rgb_img)
        if make_loop:
            points.extend(points[0])
        draw.line(points, fill=color, width=width)

    @staticmethod
    def from_grayscale_pixeldata(pixel_array, scale=255.0, dtype=np.uint8):
        if scale is not None:
            pixel_array = PixelarrayService.scale(pixel_array, factor=scale)
        img = Image.fromarray(pixel_array.astype(dtype))
        return img

    @staticmethod
    def overlay_with_color(src_img, overlay_img_list, color_list):
        assert (isinstance(overlay_img_list, list))
        assert (isinstance(color_list, list))
        assert (len(color_list) == len(overlay_img_list))

        img_rgb = Image.new("RGB", src_img.size)
        img_rgb.paste(src_img)
        for overlay, color in zip(overlay_img_list, color_list):
            assert (isinstance(color, list) and len(color) == 3)
            with Image.new("RGB", overlay.size) as overlay_rgb:

                # Converting mask into RGB
                overlay_rgb.paste(overlay)
                overlay_rgb = Image.fromarray(np.multiply(overlay_rgb, color).astype(np.uint8))

                # Paste overlay on top of the image.
                img_rgb.paste(overlay_rgb, (0, 0), mask=overlay)

        return img_rgb

    @staticmethod
    def image_to_rgb(src_img):
        return PillowService.overlay_with_color(src_img, [], [])
