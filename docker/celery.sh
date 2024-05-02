#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery --app=app.tasks.tasks:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app=app.tasks.tasks:celery flower
elif [[ "${1}" == "beat" ]]; then
  celery --app=app.tasks.tasks:celery beat
fi