import threading
from coin_api import get_tickers, metrics
from time import time

def wrapper():
    start = time()
    res = get_tickers(10, 'volume_24h')
    all_metrics.append(metrics(res))

 
passed = True; #changes to False if smth wrong
start_time = time()
all_metrics = []
threads = []
limit = 8
for i in range(limit):
    t = threading.Thread(target=wrapper) 
    threads.append(t)
    t.start()
    
for thread in threads:
    thread.join()       # waits until the thread has finished work

all_time = time()-start_time
rps = limit/all_time

tests_passed = 0
for metric in all_metrics:    #all tests are passed?
    if metric['passed']:
        tests_passed +=1

fast_response_count = 0
fast_response_time = 0.45
for metric in all_metrics:   #count latency < 450ms
    if metric['req_time'] < fast_response_time:
        fast_response_count +=1
   
fast_response_perc =  fast_response_count/limit

print ('По результатам', limit, 'параллельных / асинхронных тестов тест', end = ' ')
if tests_passed == limit and rps > 5 and fast_response_perc >=0.8:
    thread_test_passed = True
    print ('пройден')
else:
    thread_test_passed = False
    print ('не пройден')

print ('успешных тестов:', tests_passed, 'из ', limit)
print ('rps =', rps)
print ('< 450ms latency:', int(fast_response_perc*100), '%')
print ('==tests results lower==')
for metric in all_metrics:
    print (metric)

