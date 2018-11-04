from apscheduler.schedulers.blocking import BlockingScheduler
import subscription

sched = BlockingScheduler()

#@sched.scheduled_job('interval', minutes=2)
#def timed_job():
#    subscription.sendMsg()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=9)
def scheduled_job():
    subscription.sendMsg()

sched.start()
