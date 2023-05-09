from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import plotly.graph_objs as go
from datetime import datetime
from forms import PeriodForm


app = Flask(__name__, static_folder='static')
app.secret_key = 'my_secret_key'


@app.route('/FAQ')
def FAQ():
    return render_template('./FAQ.html', title='Цель существования')


@app.route('/statistic', methods=['GET', 'POST'])
def stat():
    # Считываем данные из базы данных
    conn = sqlite3.connect('police.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Criminals WHERE "case_status" = "Активно"')
    active_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM Criminals WHERE "case_status" = "Закрыто"')
    closed_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM Criminals WHERE "case_status" = "В архиве"')
    archive_count = cursor.fetchone()[0]
    conn.close()

    # Обработка формы выбора периода
    form = PeriodForm(request.form)

    if form.submit2.data:  # если кнопка "За весь период" была нажата
        return redirect(url_for('stat'))  # делаем редирект на ту же страницу без параметров

    if request.method == 'POST' and form.validate():
        start_date = form.start_date.data
        end_date = form.end_date.data

        # Преобразуем даты из формата строки в формат datetime
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())

        # Считываем данные из базы данных за выбранный период
        conn = sqlite3.connect('police.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT COUNT(*) FROM Criminals WHERE case_status = "Активно" AND Date_criminals BETWEEN ? AND ?',
            (start_date.strftime('%d.%m.%Y'), end_date.strftime('%d.%m.%Y')))
        active_count = cursor.fetchone()[0]

        cursor.execute(
            'SELECT COUNT(*) FROM Criminals WHERE case_status = "Закрыто" AND Date_criminals BETWEEN ? AND ?',
            (start_date.strftime('%d.%m.%Y'), end_date.strftime('%d.%m.%Y')))
        closed_count = cursor.fetchone()[0]

        cursor.execute(
            'SELECT COUNT(*) FROM Criminals WHERE case_status = "В архиве" AND Date_criminals BETWEEN ? AND ?',
            (start_date.strftime('%d.%m.%Y'), end_date.strftime('%d.%m.%Y')))
        archive_count = cursor.fetchone()[0]

        conn.close()

        # Обновляем данные на графике
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=['Активно'], y=[active_count], mode='lines+markers', name='Активно'))
        fig.add_trace(go.Scatter(x=['В архиве'], y=[archive_count], mode='lines+markers', name='В архиве'))
        fig.add_trace(go.Scatter(x=['Закрыто'], y=[closed_count], mode='lines+markers', name='Закрыто'))
        fig.update_layout(xaxis_tickformat='%d.%m.%Y')

        fig.update_layout(
            title='Статистика дел',
            xaxis=dict(title='Статус дела'),
            yaxis=dict(title='Количество дел'),
            legend=dict(title='Статус')
        )

        # Возвращаем график в виде HTML-кода
        plot_div = fig.to_html(full_html=False)
        return render_template('./static.html', title='Статистика по преступникам', plot_div=plot_div, form=form, archive_count=archive_count, active_count=active_count, closed_count=closed_count)

    # Строим линейный график за все время
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=['Активно'], y=[active_count], mode='lines+markers', name='Активно'))
    fig.add_trace(go.Scatter(x=['В архиве'], y=[archive_count], mode='lines+markers', name='В архиве'))
    fig.add_trace(go.Scatter(x=['Закрыто'], y=[closed_count], mode='lines+markers', name='Закрыто'))
    fig.update_layout(xaxis_tickformat='%d.%m.%Y')

    # Возвращаем график и форму выбора периода в виде HTML-кода
    plot_div = fig.to_html(full_html=False)
    return render_template('./static.html', title='Статистика по преступникам', plot_div=plot_div, form=form, archive_count=archive_count, active_count=active_count, closed_count=closed_count)


@app.route('/table')
def table():
    conn = sqlite3.connect('police.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Criminals")
    rows = cur.fetchall()
    conn.close()
    return render_template('./table.html', title='Таблица по преступникам', rows=rows)

@app.route('/news')
def news():
    conn = sqlite3.connect('police.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM News")
    news = cur.fetchall()
    conn.close()
    return render_template('./news.html', title='Криминальные новости', news=news)

@app.route('/base')
def base():
    return render_template('./index.html', title='Главная страница')

@app.route('/search')
def search():
    query = request.args.get('query')
    conn = sqlite3.connect('police.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Criminals WHERE last_name LIKE ? OR first_name LIKE ? OR fathers_name LIKE ? OR article LIKE ? OR about_article LIKE ? OR investigator LIKE ? OR case_status LIKE ?", ('%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%'))
    results = cur.fetchall()
    return render_template('search_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)