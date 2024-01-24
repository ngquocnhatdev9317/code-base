FROM python:3.10 AS compiler
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur requirements.txt

FROM python:3.10 AS runner
WORKDIR /app/
COPY --from=compiler /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app/
WORKDIR /app/src/

CMD [ "gunicorn", "main:create_app", "--bind", "0.0.0.0:8080", "--worker-class", "aiohttp.GunicornWebWorker" ]
