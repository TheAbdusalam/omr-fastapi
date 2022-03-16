import cv2 as cv
import numpy as np


def processImage(file_name):
    """
    Processes the image and saves convert it to a new cv image
    """
    default_dir = "temp/images/"
    image = cv.imread(default_dir + file_name)

    return image


def rectContour(contours):
    """
    Returns the biggest contours that in the rectangle
    """
    rectCon = []
    for i in contours:
        area = cv.contourArea(i)
        if area > 50:
            peri = cv.arcLength(i, True)
            approx = cv.approxPolyDP(i, 0.02 * peri, True)
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv.contourArea, reverse=True)

    return rectCon[0]  # 0 = the biggest contour


def getCornerPoints(contour):
    """
    Returns the four corner points of the contour
    """
    points = cv.arcLength(contour, True)
    approximation = cv.approxPolyDP(contour, 0.02 * points, True)

    return approximation


def reoOrderContourPoints(points):
    """
    Reorders the corner points to the correct order
    """
    points = points.reshape((4, 2))
    newPoints = np.zeros((4, 1, 2), np.int32)
    add = points.sum(1)

    newPoints[0] = points[np.argmin(add)]  # [0,0]
    newPoints[3] = points[np.argmax(add)]  # [w,h]
    diff = np.diff(points, axis=1)

    newPoints[1] = points[np.argmin(diff)]  # [w,0]
    newPoints[2] = points[np.argmax(diff)]  # [h,0]

    return newPoints


def extractedChosenAnswers(threshold, questions, choices):
    """
    Returns the extracted answers from the image
    """
    questions_list = np.vsplit(threshold, questions)
    answers = np.zeros((questions, choices), np.float32)
    q_count = 0

    for i in questions_list:
        choice_list = np.hsplit(i, choices)

        for j in range(0, choices):
            answers[q_count, j] = np.count_nonzero(choice_list[j])

        q_count += 1

    selected_answers = answers.argmax(axis=1)
    return selected_answers
