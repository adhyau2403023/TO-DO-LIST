from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
TASK_FILE = "tasks.txt"

def read_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            tasks = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        tasks = []
    return tasks

def write_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

@app.route("/", methods=["GET", "POST"])
def home():
    tasks = read_tasks()
    if request.method == "POST":
        task = request.form["task"]
        if task:
            tasks.append(task)
            write_tasks(tasks)
        return redirect(url_for("home"))
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = read_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        write_tasks(tasks)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
