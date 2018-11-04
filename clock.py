from apscheduler.schedulers.blocking import BlockingScheduler
import subscription

sched = BlockingScheduler()

@sched.scheduled_job('interval', days=1)
def timed_job():
    subscription.sendMsg()

@sched.scheduled_job('cron', day_of_week='0-6', hour=19)
def scheduled_job():
    subscription.sendMsg()

sched.start()
