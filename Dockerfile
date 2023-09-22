FROM python:3.10.6
ADD parser.py .
ADD db.py .
ADD requirements .
RUN pip install -r requirements --no-cache-dir && rm -f requirements && python db.py
CMD python parser.py