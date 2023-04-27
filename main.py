from flask import Flask, render_template, g, request
import psutil
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)
b_sent = 0
b_recv = 0


@app.before_request
def before_request():
    # g.bytes_received = 0
    # g.bytes_sent = 0
    pass


@app.after_request
def after_request(response):
    global b_sent
    global b_recv

    response.direct_passthrough = False
    b_sent += request.content_length or 0
    b_recv += len(response.data)
    # print(b_sent, b_recv)
    return response


@app.route('/')
def index():
    # Get the CPU usage
    cpu_usage = psutil.cpu_percent()

    # Get the memory usage
    memory_usage = psutil.virtual_memory().percent

    # Get the bytes sent and received
    # net_io_counters = psutil.net_io_counters()
    bytes_sent = b_sent//8
    bytes_recv = b_recv//8

    # Create a graph of the CPU usage and memory usage
    fig, ax = plt.subplots()
    ax.plot([cpu_usage, memory_usage])
    ax.set_xticklabels(['', 'CPU', '', 'Memory'])
    ax.set_ylabel('Usage (%)')
    ax.set_ylim([0, 100])

    # Save the graph to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the buffer to base64
    graph = base64.b64encode(buffer.getvalue()).decode()

    # Render the template with the statistics and graph
    return render_template('index.html', cpu_usage=cpu_usage, memory_usage=memory_usage, bytes_sent=bytes_sent, bytes_recv=bytes_recv, graph=graph)


@app.route('/image')
def image():
    return render_template("image.html")

if __name__ == '__main__':
    app.run()
