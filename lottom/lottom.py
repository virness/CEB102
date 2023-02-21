from flask import Flask, render_template
import random

app = Flask(__name__)

def get_bonus_results():
    bonus_results = []
    for i in range(1, 8):
        bonus = random.randint(1, 8)
        bonus_results.append((i, bonus))
    return bonus_results

@app.route("/")
def index():
    numbers = [i for i in range(1, 40)]
    results = []
    for i in range(1, 9):
        if i < 8:
            draw = random.sample(numbers, 5)
            for number in draw:
                numbers.remove(number)
        else:
            draw = random.sample(numbers, 4)
            draw += random.sample([i for i in range(1, 40)], 1)
        results.append((i, sorted(draw)))
    return render_template("index.html",  results=results)

@app.route("/lottom")
def lottom():
    results = []
    for i in range(1, 8):
        if i < 7:
            draw = random.sample(range(1, 39), 6)
            results.append((i, sorted(draw)))
        else:
            # 第七次抽取前兩個不可以跟前六次的數字相同
            while True:
                draw = random.sample(range(1, 39), 6)
                if not any([set(draw[:2]) == set(res[1][:2]) for res in results]):
                    break
            results.append((i, sorted(draw)))
    bonus_results = []
    for i in range(1, 8):
        bonus = random.randint(1, 8)
        bonus_results.append((i, bonus))

    return render_template("lottom.html", results=results, bonus_results=bonus_results)

@app.route("/biglottom")
def biglottom():
    results = []
    for i in range(1,10,1):
        if i < 9:
            draw = random.sample(range(1, 49), 6)
            results.append((i, sorted(draw)))
        else:
            while True:
                draw = random.sample(range(1, 49), 6)
                if not any([set(draw[:2]) == set(res[1][:2]) for res in results]):
                    break
            results.append((i, sorted(draw)))

    return render_template("lottom.html", results=results)

def today539():
    numbers = [i for i in range(1, 40)]
    results = []
    for i in range(1, 9):
        if i < 8:
            draw = random.sample(numbers, 5)
            for number in draw:
                numbers.remove(number)
        else:
            draw = random.sample(numbers, 4)
            draw += random.sample([i for i in range(1, 40)], 1)
        results.append((i, sorted(draw)))
    return results

if __name__ == "__main__":
    app.run()
