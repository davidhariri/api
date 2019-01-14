from helpers.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from models.base import Base
from enum import Enum
from PIL import Image, ExifTags
from colorthief import ColorThief
import moviepy.editor as mp
import os


class InvalidMediaTypeException(Exception):
    pass


# Overrides init of ColorThief to pass in the buffer from memory
class ColorThiefFromImage(ColorThief):
    def __init__(self, image):
        self.image = image


class MediaType(Enum):
    PNG = "image/png"
    JPG = "image/jpg"
    JPEG = "image/jpeg"
    GIF = "image/gif"

    def ext(self):
        return self.value.split("/")[1]


STATIC_MEDIA_TYPES = set([MediaType.PNG, MediaType.JPG, MediaType.JPEG])

OPTIMAL_CANVAS_SIZE = 896, 896
OPTIMAL_QUALITY = 80
DEFAULT_AVG_COLOR = "#eff1f3"

EXIF_NAME_MAPS = {
    "LEICA Q (Typ 116)": "Q",
    "LEICA CAMERA AG": "Leica"
}

# filename format: <ASPECT>_<COLOR>_<UUID><".thumb"?>.<FMT>
MEDIA_NAME = "{}_{}_{}{}.{}"


class Media(Base):
    """
    A media object, like an image or a video
    """

    __tablename__ = "media"

    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    media_type = db.Column(db.Enum(MediaType), nullable=False)
    url = db.Column(db.String, nullable=False)
    url_optimized = db.Column(db.String, nullable=False)
    url_poster = db.Column(db.String)
    showcase = db.Column(db.Boolean, default=False, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    aspect = db.Column(db.String, nullable=False)
    shot_exposure = db.Column(db.String)
    shot_aperture = db.Column(db.String)
    shot_speed = db.Column(db.String)
    shot_focal_length = db.Column(db.String)
    camera_make = db.Column(db.String)
    camera_model = db.Column(db.String)
    average_color = db.Column(db.String)

    def __init__(self, file):
        self.file = file

        # Try to cast the file_type as a MediaType
        try:
            self.media_type = MediaType(file.content_type)
        except Exception:
            raise InvalidMediaTypeException(
                "Sorry '{}' is not a supported format".format(
                    file.content_type))

        self.uuid = uuid.uuid4()

    def set_exif(self):
        image = Image.open(self.file)

        try:
            exif = {
                ExifTags.TAGS[k]: v
                for k, v in image._getexif().items()
                if k in ExifTags.TAGS
            }
        except Exception:
            return

        exposure = exif.get("ExposureTime", None)

        if exposure is not None:
            self.shot_exposure = "{}/{}".format(exposure[0], exposure[1])

        aperture = exif.get("FNumber", None)

        if aperture is not None:
            self.shot_aperture = "ƒ{}".format(round(aperture[0] / aperture[1], 1))

        self.shot_speed = exif.get("ISOSpeedRatings", None)

        self.shot_focal_length = str(exif.get("FocalLengthIn35mmFilm", None)) + "mm"

        self.camera_make = exif.get("Make", None)
        self.camera_model = exif.get("Model", None)

        self.camera_make = EXIF_NAME_MAPS.get(self.camera_make, self.camera_make)
        self.camera_model = EXIF_NAME_MAPS.get(self.camera_model, self.camera_model)

        pass

    def set_static_info(self):
        image = Image.open(self.file)

        self.width = image.width
        self.height = image.height

        self.aspect = str(round(self.width / self.height, 2))

    def optimize(self):
        if self.media_type in STATIC_MEDIA_TYPES:
            self.set_static_info()
            self.set_exif()

            return self.optimize_static()

        elif self.media_type is MediaType.GIF:
            return self.optimize_gif()

        else:
            raise Exception("Called optimize on media that cannot be optimized")

    def set_average_color(self, image):

        def rgb_to_hex(rgb):
            return '%02x%02x%02x' % rgb

        try:
            color_thief = ColorThiefFromImage(image)
            avg_color = rgb_to_hex(color_thief.get_color(quality=1))
        except Exception:
            self.average_color = DEFAULT_AVG_COLOR

            return DEFAULT_AVG_COLOR

        self.average_color = avg_color

        return avg_color

    def optimize_gif(self):
        # Save GIF to FS
        raw_gif_file_name = str(self.uuid) + "." + self.media_type.ext()
        self.file.save(raw_gif_file_name)

        # Cast GIF to Clip
        clip = mp.VideoFileClip(raw_gif_file_name)

        temp_poster_file_name = str(self.uuid) + ".poster.jpeg"
        clip.save_frame(temp_poster_file_name, t=0)
        poster = Image.open(temp_poster_file_name)

        self.set_average_color(poster)

        self.width = clip.w
        self.height = clip.h
        self.aspect = round(self.width / self.height, 2)

        # Save optimized MP4 clip
        optimized_mp4_filename = MEDIA_NAME.format(
            self.aspect,
            self.average_color,
            self.uuid,
            ".thumb",
            "mp4")

        clip.write_videofile(
            optimized_mp4_filename,
            codec="libx264",
            bitrate="3000k",
            progress_bar=False,
            verbose=False,
            ffmpeg_params=["-movflags", "faststart", "-pix_fmt", "yuv420p", "-vf", "scale=896:-2"])

        gif_file_name = MEDIA_NAME.format(
            self.aspect,
            self.average_color,
            self.uuid,
            "",
            self.media_type.ext())

        os.rename(raw_gif_file_name, gif_file_name)

        # Make poster
        poster_jpeg_file_name = MEDIA_NAME.format(
            self.aspect,
            self.average_color,
            self.uuid,
            ".poster",
            "jpeg")

        os.rename(temp_poster_file_name, poster_jpeg_file_name)

        return [gif_file_name, optimized_mp4_filename, poster_jpeg_file_name]

    def optimize_static(self):
        # Cast as PIL Image
        image = Image.open(self.file)

        # Rotate based on EXIF data
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif = dict(image._getexif().items())

            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)

            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)

            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)

        except (AttributeError, KeyError, IndexError):
            pass

        # Convert to JPG and reduce quality
        image = image.convert('RGB')

        # Generate smaller thumbnail
        image_thumb = image.copy()
        image_thumb.thumbnail(OPTIMAL_CANVAS_SIZE, Image.ANTIALIAS)

        self.set_average_color(image_thumb)

        raw_image_file_name = MEDIA_NAME.format(
            self.aspect,
            self.average_color,
            self.uuid,
            "",
            self.media_type.ext())

        image.save(
            raw_image_file_name,
            format=self.media_type.name)

        optimized_image_file_name = MEDIA_NAME.format(
            self.aspect,
            self.average_color,
            self.uuid,
            ".thumb",
            "jpeg")

        image_thumb.save(
            optimized_image_file_name,
            quality=OPTIMAL_QUALITY,
            format=self.media_type.name)

        return [raw_image_file_name, optimized_image_file_name]
