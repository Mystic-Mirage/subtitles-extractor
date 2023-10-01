FROM python:3.11-slim

ENV DEBIAN_FRONTEND noninteractive
ENV PIP_NO_CACHE_DIR 1
ENV PIP_ROOT_USER_ACTION ignore
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg

VOLUME /media
VOLUME /data
ENV SUBTITLES_EXTRACTOR_LIBRARIES /media
ENV SUBTITLES_EXTRACTOR_SLEEP 1
ENV SUBTITLES_EXTRACTOR_FORCED_ONLY 0
ENV SUBTITLES_EXTRACTOR_SKIP_SRT 0
ENV SUBTITLES_EXTRACTOR_STRIP_FORMATTING 0
ENV SUBTITLES_EXTRACTOR_LANGUAGES *
ENV SUBTITLES_EXTRACTOR_DATA_DIR /data

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "-m", "subtitles_extractor"]
