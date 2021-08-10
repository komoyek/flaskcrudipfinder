import ipapi
from datetime import datetime
import threading
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM
import time
from flask import Flask, request, render_template

#pip install ipapi


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def Index():
    return render_template('index.html')


@app.route('/pgen', methods = ['GET', 'POST'])
def Pgen():
    return render_template('pgen.html')

@app.route('/search', methods = ['GET', 'POST'])
def Search():
    return render_template('search.html')

@app.route('/result', methods = ['GET', 'POST'])
def result():
    search = request.form.get('search')
    data = ipapi.location(ip=search, output='json')
    return render_template('result.html', data=data)


@app.route('/search2', methods = ['GET', 'POST'])
def search():
    return render_template('search2.html')

@app.route('/portscan', methods = ['GET', 'POST'])

def portx():
    start_time = datetime.now()  # port scan start time

    print_lock = threading.Lock()

    cible = request.form.get('search')
    data = []
    temps= []
    def portscan(port):
        s = socket(AF_INET, SOCK_STREAM)

        try:
            con = s.connect((cible, port))
            with print_lock:
                data.append(port)

            con.close()
        except:
            pass

    def Threader():
        while True:
            worker = q.get()

            portscan(worker)

            q.task_done()

    q = Queue()

    for x in range(30):
        t = threading.Thread(target=Threader)

        t.daemon = True

        t.start()

    start = time.time()

    for worker in range(1, 100):
        q.put(worker)

    q.join()

    end_time = datetime.now()  # port scan ends: mark time
    duration = end_time - start_time  # port scan duration
    temps.append(f'Le scan à duré : {round(duration.total_seconds(), 2)} secondes')
    return render_template('portscan.html', data=data, temps=temps, address=cible)




if __name__ == "__main__":
    app.run(debug = False)
