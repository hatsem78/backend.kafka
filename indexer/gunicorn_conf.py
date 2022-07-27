# Importar multiprocessing si se va a usar mucho recurso
# import multiprocessing
backlog = 2048

bind = '0.0.0.0:8007'
workers = 4  # multiprocessing.cpu_count()
timeout = 340
threads = 3
max_requests = 1000
concurrency = 2
worker_connections = 30
max_requests = 1000
max_requests_jitter = 100
