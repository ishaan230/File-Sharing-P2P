( bash -c "cd p2pbackend && source ./venv/bin/activate && pip install -r requirements.txt && flask --app server.py --debug run &" ) ; ( bash -c "cd frontend && npm run tauri dev &" )
