from flask import Flask, render_template
import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt1
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)



def plot_line_graph():
    data = [10, 20, 30, 60, 57, 60, 70, 70, 90, 100]

    plt1.plot(data, marker='o', color='#9C90D2FF')
    plt1.title('Статистика по всем выполненым работам')
    plt1.xlabel('Номеры работы')
    plt1.ylabel('Процент выполнения')
    plt1.ylim(0, 100)
    plt1.xlim(1, len(data)-1)
    plt1.grid()
    plt1.show()

    #plt1.savefig('static/media/chart.png', bbox_inches='tight')
    plt1.close()

    return plt1


def plot_stolb():
    data = {
        1: [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1,
            1, 0, 1, 1, 0],
        2: [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1,
            1, 0, 1, 0, 1],
        3: [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1,
            1, 0, 1, 0, 1],
        4: [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1,
            1, 0, 1, 0, 1],
        5: [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1,
            1, 0, 1, 0, 1],
    }

    total_attempts = len(data)
    task_completion = [0] * 27

    for work in data.values():
        for i in range(len(work)):
            task_completion[i] += work[i]

    task_completion_percentage = [(x / total_attempts) * 100 for x in
                                  task_completion]

    plt2.figure(figsize=(10, 6))
    plt2.bar(range(1, 28), task_completion_percentage, color='9C90D2FF')
    plt2.xlabel('Номер задания')
    plt2.ylabel('Статистика по всем выполненым работам')
    plt2.title('Анализ успеваемости по заданиям')
    plt2.xticks(range(1, 28))

    return plt2



@app.route('/')
def index():

    return render_template('1.html')



if __name__ == '__main__':
    plt = plot_line_graph()
    plt.show()
    #plt.savefig('static/media/chart.png')
    plt.close()

