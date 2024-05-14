# Machine Learning Emotion Diary

## What is this?

This is my Year 13 Project that uses machine learning to analyze diary entries submitted and detect emotions. This can then be stored on a MySQL database and pulled down for futher analysis.
It's built using Python, Typescript, and MySQL. 
I've kept it up as I felt there weren't enough example projects out there, and so wanted to have mine up as an example. Whilst it's not the best, it's a good middle of the road example. As part of this project, I've provided the original Write-Up as well, so you can look at that if you so wish. I've also broken down how many marks are in each section, and the grade the project as a whole got. 
I hope that people find this helpful, and can learn from my successes, as well as all the mistakes I made. This branch will not be changing as to preserve it as a resource. This project will also be redone on the main branch, so if you want to see it done better, check out the master branch.

## How to run?

For dev work, you'll need to install the dependancies.

For the frontend, you'll need to run `pnpm install` in the `frontend` directory.

For the backend, you'll need to run `pip install -r requirements.txt` in the `backend` directory.

Then you can run the frontend with `pnpm dev` in the `frontend` directory and the backend with `uvicorn fastApi:app --reload` in the `backend` directory.

You'll need to provide you're own .env file for the database connection.

## License?

None yet, will make it open source at the end of Year 13.
