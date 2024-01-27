FROM python:3.11.5

COPY . .

RUN pip install poetry==1.6.1
RUN poetry install
RUN mv build/lib.linux*/mapanalyzerext.*.so mapanalyzerext.so

CMD ["/bin/bash"]
