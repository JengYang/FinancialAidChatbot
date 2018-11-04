from apscheduler.schedulers.blocking import BlockingScheduler
import subscription

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=2)
def timed_job():
    subscription.sendMsg()

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
#def scheduled_job():
#    print('This job is run every weekday at 5pm.')

sched.start()
