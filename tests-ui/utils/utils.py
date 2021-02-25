# pylint: disable=import-outside-toplevel
# pylint: disable=no-member
import errno
import json
import math
import os
import re
from functools import reduce
from os import path, strerror
from pathlib import Path
from datetime import datetime, date
from datetime import timedelta
import pytest
from selenium.webdriver.support.color import Color


def get_env_name(caps: dict):
    os = caps['os'] if 'os' in caps else None
    os_version = caps['os_version'] if 'os_version' in caps else ''
    env = caps['browser'] if 'browser' in caps else caps['device'] if 'device' in caps else 'Chrome'

    if os is None:
        env_name = '%s - %s' % (env, os_version)
    else:
        env_name = '%s %s - %s' % (os, os_version, env)
    print('Test results will be exported to "%s" TestRail Configuration' % env_name)
    return env_name


def initialize_screenshot_dirs(root_dir):
    pytest.globalDict['base_screenshot_dir'] = root_dir + '/screenshots/base'
    pytest.globalDict['actual_screenshot_dir'] = root_dir + '/screenshots/actual'
    pytest.globalDict['diff_screenshot_dir'] = root_dir + '/screenshots/diff'


def read_file(file_name):
    # file_path = re.sub(r'utils.(\w+)', file_name, path.abspath(__file__))
    file_path = get_file_path(file_name)
    with open(file_path, encoding="utf-8") as fl:
        extension = path.splitext(file_path)[1]
        if extension == '.json':
            raw_data = json.load(fl)
            return raw_data
        if extension == '.txt':
            raw_data = fl.read()
            return raw_data
        raise extension


def get_file_path(file_name):
    path_object = Path(file_name)
    if not path_object.exists():
        raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), file_name)
    return path_object.resolve()


def compare_images(image_b, base_screenshot_url, actual_screenshot_url, diff_screenshot_url=None, base_score=1):
    from skimage.metrics import structural_similarity
    import imutils
    import cv2

    # load the two input images
    if image_b is None:
        image_b = cv2.imread(actual_screenshot_url)
    image_a = cv2.imread(base_screenshot_url)
    if image_a is None:
        os.makedirs(actual_screenshot_url[:actual_screenshot_url.rfind('/')], exist_ok=True)
        cv2.imwrite(actual_screenshot_url, image_b)
        raise AssertionError('There is no base image for: %s' % base_screenshot_url)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned

    if image_a.shape != image_b.shape:
        height, width, channels = image_b.shape
        image_a = cv2.resize(image_a, (width, height), interpolation=cv2.INTER_AREA)
        # os.makedirs(actual_screenshot_url[:actual_screenshot_url.rfind('/')], exist_ok=True)
        # cv2.imwrite(actual_screenshot_url, image_b)
        # raise AssertionError(
        #     'Base: %s and\n Actual: %s\n have different sized' % (base_screenshot_url, actual_screenshot_url))

    # convert the images to grayscale
    gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    (score, diff) = structural_similarity(gray_a, gray_b, full=True)
    if score < base_score and diff_screenshot_url is not None:
        os.makedirs(actual_screenshot_url[:actual_screenshot_url.rfind('/')], exist_ok=True)
        os.makedirs(diff_screenshot_url[:diff_screenshot_url.rfind('/')], exist_ok=True)
        cv2.imwrite(actual_screenshot_url, image_b)
        diff = (diff * 255).astype("uint8")

        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for cnt in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            (x_point, y_point, width, height) = cv2.boundingRect(cnt)
            cv2.rectangle(image_b, (x_point, y_point), (x_point + width, y_point + height), (0, 0, 255), 2)

        cv2.imwrite(diff_screenshot_url, image_b)

    return score


def get_horizontal_spacing(elem_1, elem_2):
    spacing = 0  # TODO

    return spacing


def get_vertical_spacing(elem_1, elem_2):
    spacing = 0  # TODO

    return spacing


def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


def deep_get(dictionary, *keys):
    return reduce(lambda d, key: d.get(key) if d else None, keys, dictionary)

def set_mtp_date_to_week_day(mtp_date):
    MTP_date = str(mtp_date)        #strDate.strftime('%d/%m/%Y')
    # print(Todays_date)
    date_time_obj = datetime.strptime(MTP_date, '%d/%m/%Y')
    if date_time_obj.isoweekday() == 6:
        date_time_obj += timedelta(days=2)
    elif date_time_obj.isoweekday() == 7:
        date_time_obj += timedelta(days=1)
    else:
        date_time_obj += timedelta(days=0)
    return datetime.strftime(date_time_obj, '%d/%m/%Y')
    