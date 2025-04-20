from celery import Celery
import time
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Celery("tasks", broker="redis://localhost:6379/0")

job_status = {}

@app.task
def process_file(job_id, file_path):
    print(f"Processing file {file_path} for job {job_id}")
    try:
        with open(file_path, "r") as f:
            text = f.read()

        prompt = f"Turn this blog into a Twitter thread:\n{text}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that repurposes content."},
                {"role": "user", "content": prompt},
            ]
        )

        result = response.choices[0].message.content
        output_file = f"outputs/{job_id}.txt"
        with open(output_file, "w") as f:
            f.write(result)

        job_status[job_id] = "Done"
        print("Job done.")
    except Exception as e:
        job_status[job_id] = f"Failed: {str(e)}"
        print(f"Error: {str(e)}")
