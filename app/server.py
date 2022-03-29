from main import OMR
from fastapi import FastAPI, File, UploadFile
import uvicorn
from helpers import File as FileHelper

""" instantiate the app """
app = FastAPI()


@app.post("/")
async def serve(
    file: UploadFile = File(...),
    questions: int = None,
    choices: int = None,
    answers: str = None,
    scoring_method: str = "score_by_percentage", # score_by_weight
):
    # save the file to the temp folder
    filename = FileHelper.saveTempFile(file)

    # initialize the OMR object
    omr = OMR(
        filename,
        questions_count=questions,
        choices_count=choices,
        correct_answers=answers,
        paper_dimension=(40, 40),
    )

    # return the score based on the scoring method
    return omr.score(method=scoring_method)


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
