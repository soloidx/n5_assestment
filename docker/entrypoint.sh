#!/usr/bin/env bash

set -o errexit
set -o pipefail

MANAGE_PARAM=""

if [ -z "$APP_ENV" ]; then
  MANAGE_PARAM="--settings=n5_assessment.settings.local"
else
  if [ "$APP_ENV" = "DEV" ]; then
    MANAGE_PARAM='--settings=n5_assessment.settings.dev'
  elif [ "$APP_ENV" = "PROD" ]; then
    MANAGE_PARAM='--settings=n5_assessment.settings.prod'
  fi
fi

/app/wait

cd /app/
python manage.py migrate $MANAGE_PARAM
python manage.py collectstatic --no-input $MANAGE_PARAM
#python manage.py runserver 0.0.0.0:8000 $MANAGE_PARAM

exec "$@" $MANAGE_PARAM
