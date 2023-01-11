FROM python:3


WORKDIR /defi_IA-main

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./app.py"]

EXPOSE 5000
CMD ["bash"]

