import moon, sys

# Encoding problem in windows
# should be removed in production run
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    moon.app.run(host='0.0.0.0', port=8000)
