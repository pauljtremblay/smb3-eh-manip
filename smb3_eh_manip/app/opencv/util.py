import cv2
import numpy as np

from smb3_eh_manip.util import settings


def locate_all_opencv(
    needleImage,
    haystackImage,
    limit=10000,
    region=None,  # [x, y, width, height]
    confidence=float(settings.get("confidence", fallback=0.95)),
):
    """
    RGBA images are treated as RBG (ignores alpha channel)
    """

    confidence = float(confidence)

    needleHeight, needleWidth = needleImage.shape[:2]

    if region:
        haystackImage = haystackImage[
            region[1] : region[1] + region[3], region[0] : region[0] + region[2]
        ]
    else:
        region = (0, 0)  # full image; these values used in the yield statement
    if (
        haystackImage.shape[0] < needleImage.shape[0]
        or haystackImage.shape[1] < needleImage.shape[1]
    ):
        # avoid semi-cryptic OpenCV error below if bad size
        raise ValueError(
            "needle dimension(s) exceed the haystack image or region dimensions"
        )

    # get all matches at once, credit: https://stackoverflow.com/questions/7670112/finding-a-subimage-inside-a-numpy-image/9253805#9253805
    result = cv2.matchTemplate(haystackImage, needleImage, cv2.TM_CCOEFF_NORMED)
    match_indices = np.arange(result.size)[(result > confidence).flatten()]
    matches = np.unravel_index(match_indices[:limit], result.shape)

    if len(matches[0]) == 0:
        return

    # use a generator for API consistency:
    matchx = matches[1] + region[0]  # vectorized
    matchy = matches[0] + region[1]
    for x, y in zip(matchx, matchy):
        yield (x, y, needleWidth, needleHeight)
