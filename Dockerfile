FROM python:3.11-slim

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y --no-install-recommends ffmpeg

VOLUME /media
ENV SUBTITLES_EXTRACTOR_LIBRARIES /media
ENV SUBTITLES_EXTRACTOR_SLEEP 1
ENV SUBTITLES_EXTRACTOR_FORCED_ONLY 0
ENV SUBTITLES_EXTRACTOR_LANGUAGES *

WORKDIR /app
COPY . .

CMD ["python3", "-m", "subtitles_extractor"]
