from flask import Flask, render_template, flash, request

import datetime
from modules import File
from modules import ParseData

app = Flask(__name__)
app.config['SECRET_KEY'] = 'reds209ndsldssdsljdsldsdsljdsldksdksdsdfsfsfsfis'

TIME_DELTA = datetime.timedelta(days=1)
TODAY_DATE = datetime.datetime.now()


def string_to_date(__str: str, time_delta=False):
    __date = datetime.datetime.strptime(__str, '%Y-%m-%d')
    __date = __date.date()
    if time_delta:
        __date = (__date + TIME_DELTA)
    return __date


def date_to_path(__str):
    __date = datetime.datetime.strftime(__str, "%Y-%m")
    return __date


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/Сотрудники', methods=["POST", "GET"])
def users_view():
    users = File.users_load()
    return render_template('users_view.html', users=users.to_html(index=False))


@app.route('/Отчет')
def data_activate():
    return render_template("data_view.html", max_date=TODAY_DATE)

@app.route('/Отчет/Табель', methods=["POST", "GET"])
def data_view():
    start_date = ""
    end_date = ""
    if request.method == "POST":
        _start_date = request.form.get("start_date")
        if len(_start_date) < 2:
            flash("Выберите начало периода", "error")
            return render_template("data_view.html", max_date=TODAY_DATE)

        start_date = string_to_date(_start_date, False)
        start_date_path = date_to_path(start_date)
        _end_date = request.form.get("end_date")
        if len(_end_date) < 2:
            flash("Выберите окончание периода", "error")
            print("Выберите окончание периода")
            return render_template("data_view.html", max_date=TODAY_DATE)
        end_date = string_to_date(_end_date, True)
        end_date_path = date_to_path(end_date)
        _df_data = File.data_load(start_date_path, end_date_path)
        if len(_df_data) < 1:
            flash("Ошибка при чтении файлов", "error")
            return render_template("data_view.html", max_date=TODAY_DATE)
        __df = ParseData.parse_data(_df_data, start_date=_start_date, end_date=_end_date)
        return render_template("data_view.html", start_date=start_date, end_date=end_date,
                               max_date=TODAY_DATE, table=__df.to_html())
    else:
        flash("Не удалось прочитать период", "error")

    return render_template('data_view.html', start_date=start_date, end_date=end_date,
                           max_date=TODAY_DATE)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
