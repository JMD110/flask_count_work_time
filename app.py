from flask import Flask, request, render_template
from datetime import datetime
import json

app = Flask(__name__)


def count_time():
    wait_t = json.load(open("/storage/emulated/0/work_time/work_time.json"))
    wait = []
    for i in wait_t:
        for j in wait_t[i]:
            start_work = wait_t[i][j][0]
            after_work = wait_t[i][j][-1]
            if start_work == after_work:
                every_day = -8
            elif 18 < after_work < 18.5:
                every_day = 18 - start_work - 9.5
            else:
                every_day = after_work - start_work - 10
            wait.append(every_day)
    print wait
    resp = 0
    for every_day in wait:
        resp += every_day
    return round(resp, 2)


@app.route('/', methods=["POST", "GET"])
def index():
    now = datetime.now()
    date = dict()
    date["hour"] = now.hour
    date["min"] = now.minute
    date["day"] = now.day
    date["mon"] = now.month
    if request.method == "GET":
        resp = count_time()
        return render_template("index.html", date=date, resp=resp)
    if request.method == "POST":
        work_time = request.form["work_time"]
        my_work_time = json.load(open("/storage/emulated/0/work_time/work_time.json"))
        hour = work_time.split(":")[0].strip()
        minute = work_time.split(":")[-1].strip()

        update_time = round(int(hour) + float(minute) / 60, 2)
        my_work_time[str(now.month)] = {} if str(now.month) not in my_work_time else my_work_time[str(now.month)]
        my_work_time[str(now.month)][str(now.day)] = [] if str(now.day) not in my_work_time[str(now.month)] else \
            my_work_time[str(now.month)][str(now.day)]
        my_work_time[str(now.month)][str(now.day)].append(update_time)
        json.dump(my_work_time, open("/storage/emulated/0/work_time/work_time.json", "w"))
        resp = count_time()
        return render_template("index.html", date=date, resp=resp)


if __name__ == '__main__':
    app.run(port=10058, debug=True)
