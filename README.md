# ip_address_range_API

## for starting the web server locally

make sure you have python and pip installed

```
pip install virtualenv

python3 -m virtualenv env

. /env/bin/activate

pip install -r requirements.txt

python run_this_first.py

uvicorn main:app --reload
```

## even though docker-compose and dockerfile is provided, it will not work because of letsencrypt ssl certificate keys
