from waitress import serve
import cfaw
serve(cfaw.app, host='127.0.0.1', port=5000)

