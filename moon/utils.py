from datetime import datetime, date
from datetime import time as dtime

from moon import app

@app.template_filter('to_date')
def to_date(st):
    if isinstance(st, datetime):
        return st.strftime("%b %d, %Y")

    if isinstance(st, unicode):
        st = str(st)

    return to_datetime(st).strftime("%b %d, %Y")

@app.template_filter('to_time')
def to_time(st):
    if isinstance(st, datetime):
        return st.strftime("%H:%M")

    if isinstance(st, unicode):
        st = str(st)

    return to_datetime(st).strftime("%H:%M")

app.jinja_env.filters['to_date'] = to_date
app.jinja_env.filters['to_time'] = to_time


def to_datetime(d):
    '''
        convert everything to datetime
    '''
    if isinstance(d, date):
        return datetime.combine(d, dtime(0, 0))

    if isinstance(d, datetime):
        return d

    if d is None:
        return datetime.now();

    if d == '':
        return datetime.now();

    dt = None
    try:
        return datetime.strptime(d, "%Y-%m-%d")
    except Exception as e:
        print("Not the %Y-%m-%d " + str(e)) # 2012-02-01
        print(type(d))

    try:
        return datetime.strptime(d, "%Y-%m")
    except Exception as e:
        print("Not the %Y-%m " + str(e)) # 2012-02
        print(type(d))

    try:
        return datetime.strptime(d, "%Y-%m-%d %H:%M")
    except Exception as e:
        print("Not the %Y-%m-%d %H:%M" + str(e)) # 2012-02-01 19:00
        print(type(d))

    return datetime.now()


