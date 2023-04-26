import requests
import psutil
import csv
import time
import atexit
import os
from selenium import webdriver


# Initialize the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

# this variable helps to set the URL to be monitored
URL_TO_MONITOR = 'https://example.com'


# this function is made to find all the values of the metrics, using the psutil library of python
def get_metrics():
    # Measure response time and latency of the web server
    start_time = time.time()
    response = requests.head(URL_TO_MONITOR)
    response_time = time.time() - start_time
    latency = response.elapsed.total_seconds()

    # Measure page load time
    driver.get(URL_TO_MONITOR)
    page_load_time = driver.execute_script(
        "return (window.performance.timing.loadEventEnd - window.performance.timing.navigationStart) / 1000"
    )

    # Get system metrics - measures the metrics of the system that you are using
    cpu_percent = psutil.cpu_percent()
    mem_used = psutil.virtual_memory().used
    disk_used = psutil.disk_usage('/').used

    # Get uptime
    uptime = time.time() - psutil.boot_time()

    # Get server load
    # its tuple where the tuple contains the system load average values for the past 1,5,15,minutes, in the form of a tuple of 3 values
    # we will be using only the middle value of the tuple, hence the index[1] used

    load_average = psutil.getloadavg()[1]
    # load_average = ','.join(str(x) for x in psutil.getloadavg())
    # load_average_str = ','.join(str(x) for x in load_average)

    # Get network metrics
    net_io_counters = psutil.net_io_counters()
    bytes_sent = net_io_counters.bytes_sent
    bytes_received = net_io_counters.bytes_recv
    packets_sent = net_io_counters.packets_sent
    packets_received = net_io_counters.packets_recv

    # Get process metrics
    process = psutil.Process(os.getpid())
    cpu_process_percent = process.cpu_percent()
    mem_process_percent = process.memory_percent()

    return [response_time, latency, uptime, cpu_percent, mem_used, disk_used, load_average, bytes_sent, bytes_received, packets_sent, packets_received, cpu_process_percent, mem_process_percent, page_load_time]


def write_to_csv(metrics):
    # Write metrics to CSV file
    with open('webpage_metrics.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(metrics)


def analyze_data():
    # Load CSV data into list of lists
    data = []
    with open('webpage_metrics.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append([float(x) for x in row])
            print(row)
            # data.append([float(x) if i != 6 else tuple(float(y) for y in x.split(',')) for i, x in enumerate(row)])

    # assigning variables for each metric that is being monitored
    response_times = [row[0] for row in data]
    latencies = [row[1] for row in data]
    uptime = [row[2] for row in data]
    cpu_usage = [row[3] for row in data]
    mem_usage = [row[4] for row in data]
    disk_usage = [row[5] for row in data]
    load_average = [row[6] for row in data]
    bytes_sent = [row[7] for row in data]
    bytes_received = [row[8] for row in data]
    packets_sent = [row[9] for row in data]
    packets_received = [row[10] for row in data]
    cpu_process_percent = [row[11] for row in data]
    mem_process_percent = [row[12] for row in data]
    page_load_time = [row[13] for row in data]

    # finding the avg amount of time, since thats of use to us now

    avg_response_time = sum(response_times) / len(response_times)
    avg_latency = sum(latencies) / len(latencies)
    avg_uptime = sum(uptime) / len(uptime)
    avg_cpu_usage = sum(cpu_usage) / len(cpu_usage)
    avg_mem_usage = sum(mem_usage) / len(mem_usage)
    avg_disk_usage = sum(disk_usage) / len(disk_usage)
    avg_load_average = sum(load_average) / len(load_average)
    avg_bytes_sent = sum(bytes_sent) / len(bytes_sent)
    avg_bytes_received = sum(bytes_received) / len(bytes_received)
    avg_packets_sent = sum(packets_sent) / len(packets_sent)
    avg_packets_received = sum(packets_received) / len(packets_received)
    avg_cpu_process_percent = sum(
        cpu_process_percent) / len(cpu_process_percent)
    avg_mem_process_percent = sum(
        mem_process_percent) / len(mem_process_percent)
    avg_page_load_time = sum(page_load_time) / len(page_load_time)

    # stroing all the above values into this variable, which will print it out after calculations
    analysis = {
        'avg_response_time': avg_response_time,
        'avg_latency': avg_latency,
        'avg_uptime': avg_uptime,
        'avg_cpu_usage': avg_cpu_usage,
        'avg_mem_usage': avg_mem_usage,
        'avg_disk_usage': avg_disk_usage,
        'avg_load_average': avg_load_average,
        'avg_bytes_sent': avg_bytes_sent,
        'avg_bytes_recieved': avg_bytes_received,
        'avg_packets_sent': avg_packets_sent,
        'avg_packets_recieved': avg_packets_received,
        'avg_cpu_process_percent': avg_cpu_process_percent,
        'avg_mem_process_percent': avg_mem_process_percent,
        'avg_page_load_time': avg_page_load_time
    }

    return analysis

# atexit module helps in indicating to run the below code ,upon abort/exiting/termination of execution
# os module allows to access the file and remove it using the remove() method


@atexit.register
def delete_csv():
    # Remove contents of CSV file when program exits [ when ctrl+c is pressed]
    if os.path.exists('webpage_metrics.csv'):
        os.remove('webpage_metrics.csv')


while True:
    metrics = get_metrics()
    write_to_csv(metrics)
    time.sleep(1)  # Wait 1 second before taking next measurements

    # we can set the linit of how many agrguments it will hold in the file, and for those many lines, the analysis is done
    if len(open('webpage_metrics.csv').readlines()) >= 10:
        analysis = analyze_data()
        print(analysis)


# idk where exactly ac
