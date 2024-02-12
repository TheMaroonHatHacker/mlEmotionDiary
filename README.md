# Machine Learning Emotion Diary

## What is this?

This is my Year 13 Project that uses machine learning to analyze diary entries submitted and detect emotions. This can then be stored on a MySQL database and pulled down for futher analysis.

It's built using Python and Typescript.

## How to run?

Currently that is a bit messy. The way I currently do it on my dev machine is open `frontend/` and `backend/` in two separate terminals, then in the `frontend/` folder run
```bash
pnpm dev
```
and in the `backend/` folder run
```bash
uvicorn fastAPI:app --reload
```
Even then, not guaranteed, I haven't really been able to get this running on any other machine than my own laptop, so still lots of work need to be done in streamlining this, however as I'm really only judged on code, not the actual deployed project, this is the bottom of my priority.

## License?

None yet, will make it open source at the end of Year 13.
