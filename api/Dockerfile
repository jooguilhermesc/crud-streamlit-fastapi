
FROM python:3.9

# remember to expose the port your app'll be exposed on.
EXPOSE 8081

RUN pip install -U pip

COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

# copy into a directory of its own (so it isn't in the toplevel dir)
COPY . /app
WORKDIR /app

# run it!
ENTRYPOINT ["fastapi", "run", "main.py", "--port", "8081"]