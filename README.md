# Machine Learning Emotion Diary

## What is this?

This is my Year 13 Project that uses machine learning to analyze diary entries submitted and detect emotions. This can then be stored on a MySQL database and pulled down for futher analysis.

It's built using Python and Typescript.

## How to run?

For dev work, you'll need to install the dependancies.

For the frontend, you'll need to run `pnpm install` in the `frontend` directory.

For the backend, you'll need to run `pip install -r requirements.txt` in the `backend` directory.

Then you can run the frontend with `pnpm dev` in the `frontend` directory and the backend with `uvicorn fastApi:app --reload` in the `backend` directory.

You'll need to provide you're own .env file for the database connection.

## License?

None yet, will make it open source at the end of Year 13.
