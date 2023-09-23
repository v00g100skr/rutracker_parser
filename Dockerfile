FROM python:3.10.6
ADD parser.py .
ADD requirements .
RUN pip install -r requirements --no-cache-dir && rm -f requirements
WORKDIR /
RUN mkdir parser_data && touch parser_data/parser.db
CMD python parser.py