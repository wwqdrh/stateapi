FROM python:3.10-slim AS builder

RUN apt update && apt install -y gcc git

RUN pip install poetry

RUN poetry config virtualenvs.in-project true

WORKDIR app

COPY . .

RUN poetry install --with=build

RUN /app/.venv/bin/python -m nuitka --module stateapi --include-package=stateapi --include-package=pykit --output-dir=dist \
    && poetry export --without-hashes -o dist/requirements.txt \
    && rm -rf dist/*.build \
    && cp -rf ./dist ./build \
    && sed -i '/^pykit/d'  ./build/requirements.txt

# production
FROM python:3.10-slim

WORKDIR app

COPY --from=builder /app/build .

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "-c", "import stateapi; stateapi.main()"]