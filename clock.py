from apscheduler.schedulers.blocking import BlockingScheduler
import subscription

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='0-6', hour=21)
def scheduled_job():
    subscription.sendMsg()

sched.start()
