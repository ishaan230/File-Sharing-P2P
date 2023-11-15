( bash -c "cd p2pbackend && source ./venv/bin/activate && pip install -r requirements.txt && python server.py &" ) ; ( bash -c "cd frontend && npm run dev &" )
