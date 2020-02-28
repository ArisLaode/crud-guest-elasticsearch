# specification
  - python = 3.5.2
  - elasticsearch = 6.3.1
  - gunicorn = 19.9.0
  - Flask = 1.1.1

# Runing
  - App Flask : gunicorn --preload -w 1 -b 0.0.0.0:18000 crud_guest:app
  - Unittesting crud guest : python -m unittest test.py
  - Unittesting elasticsearch : python -m unittest test_crud_elasticsearch.py
