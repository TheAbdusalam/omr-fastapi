import cv2 as cv
import numpy as np
from helpers.Processing import (
    processImage,
    rectContour,
    getCornerPoints,
    reoOrderContourPoints,
    extractedChosenAnswers,
)
import helpers.File as FileHelper
from services.Scoring import Scoring


class OMR:
    def __init__(
        self, file, questions_count, choices_count, correct_answers, paper_dimension
    ):
        self.image = file
        self.questions = questions_count
        self.choices = choices_count
        self.correct_answers = correct_answers
        self.paper_dimensions = paper_dimension
        self.height = paper_dimension[0] * questions_count
        self.width = paper_dimension[1] * choices_count
        self.modified_image = processImage(self.image)

    def getImageContours(self):
        image = processImage(self.image)

        # get the image contours
        grayImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        blurredImage = cv.GaussianBlur(grayImage, (5, 5), 0)

        cannyImage = cv.Canny(blurredImage, 10, 70)
        contours, _ = cv.findContours(
            cannyImage, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE
        )

        cv.drawContours(self.modified_image, contours, -1, (0, 255, 0), 5)
        return contours

    def correctPrespective(self):
        rectangles = rectContour(self.getImageContours())
        cornerPoints = getCornerPoints(rectangles)

        # reorder the corner points
        orderedPoints = reoOrderContourPoints(cornerPoints)

        # draw the container
        cv.drawContours(self.modified_image, [orderedPoints], -1, (0, 255, 0), 5)

        # get the perspective transformation matrix
        source_point = np.float32(orderedPoints)
        destination_point = np.float32(
            [[0, 0], [self.width, 0], [0, self.height], [self.width, self.height]]
        )

        matrix = cv.getPerspectiveTransform(source_point, destination_point)
        return matrix

    def getWrappedImage(self):
        matrix = self.correctPrespective()
        wrappedImg = cv.warpPerspective(
            self.modified_image, matrix, (self.width, self.height)
        )
        return wrappedImg

    def getThresholdImage(self):
        img = self.getWrappedImage()
        grayImage = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        threshold = cv.threshold(grayImage, 170, 255, cv.THRESH_BINARY_INV)[1]
        return threshold

    def extractChoices(self):
        threshold = self.getThresholdImage()
        response = extractedChosenAnswers(threshold, self.questions, self.choices)

        return response

    def score(self, method="score_by_percentage", weight=1) -> Scoring:
        selected_answers = self.extractChoices()
        score = 0
        correct_answers = list(self.correct_answers.split(","))
        correct_answers = [int(i) for i in correct_answers]

        for i in range(len(correct_answers)):
            if selected_answers[i] == correct_answers[i]:
                score += 1

        # delete the temp file
        FileHelper.deleteTempFile(self.image)

        if method == "score_by_percentage":
            scoring = Scoring(score, self.questions)
            scoring.percentage

        elif method == "score_by_weight":
            scoring = Scoring(score, self.questions, weight)
            scoring.weight

        return str(scoring)
