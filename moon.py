import moon, sys

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    moon.app.run(host='0.0.0.0', port=8000)
