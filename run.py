from api import *
import os

if __name__ == '__main__':
    # app.run(debug=True, threaded=True, port=5050)
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
