# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

FROM python:3.10

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install ffmpeg -y

RUN pip install -r requirements.txt

CMD ["python", "main.py"]

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
