FROM python:3.10

WORKDIR /app
EXPOSE 8000

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get install -y espeak espeak-data libespeak1 libespeak-dev && \
    apt-get install -y festival* && \
    apt-get install -y build-essential && \
    apt-get install -y flac libasound2-dev libsndfile1-dev vorbis-tools && \
    apt-get install -y libxml2-dev libxslt-dev zlib1g-dev

COPY . .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install aeneas

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]