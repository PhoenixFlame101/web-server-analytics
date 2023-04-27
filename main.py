from flask import Flask, render_template
import psutil
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)


@app.route('/')
def index():
    # Get the CPU usage
    cpu_usage = psutil.cpu_percent()

    # Get the memory usage
    memory_usage = psutil.virtual_memory().percent

    # Get the bytes sent and received
    net_io_counters = psutil.net_io_counters()
    bytes_sent = net_io_counters.bytes_sent
    bytes_recv = net_io_counters.bytes_recv

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


if __name__ == '__main__':
    app.run()
