from main import OMR
from fastapi import FastAPI, File, UploadFile, Request
import uvicorn
from helpers import File as FileHelper

""" instantiate the app """
app = FastAPI()

@app.post("/")
async def serve(file: UploadFile = File(...), questions: int = None, choices: int = None, answers: str = None):
    # save the file to the temp folder
    filename = FileHelper.saveTempFile(file)

    # return response
    omr = OMR(filename, questions_count=questions, choices_count=choices, correct_answers=answers, paper_dimension=(40, 40))
    return omr.score()

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
