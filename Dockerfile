FROM python:3.9-alpine
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir "nonebot[scheduler]" -i https://pypi.tuna.tsinghua.edu.cn/simple\
  && pip install -r ./awesomeBot/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["python", "./awesomeBot/bot.py"]