import schedule


def fun1():
    print('hello')
schedule.every(5).seconds.do(fun1)
while 1 :
    schedule.run_pending()
