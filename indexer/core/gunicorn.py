# Importar multiprocessing si se va a usar mucho recurso
# import multiprocessing
backlog = 2048

bind = '0.0.0.0:8091'
workers = 2  # multiprocessing.cpu_count()
timeout = 240
threads = 1
max_requests = 1000
concurrency = 2
worker_connections = 30
max_requests = 1000
max_requests_jitter = 100

errorlog = '-'
loglevel = 'info'
accesslog = '-'
