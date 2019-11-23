    #!/bin/bash
    git clone https://github.com/alexlucaci/shopIT-backend
    cd shopIT-backend
    git pull
    if [ -d "venv" ]
    then
        echo "venv exists"
    else
        python -m virtualenv venv
    fi
    source venv/bin/activate
    python3 pip install -r requirements.txt
    killall python3
    python3 manage.py migrate
    python3 manage.py runserver 0.0.0.0:8080
