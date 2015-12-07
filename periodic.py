from djcelery.models import PeriodicTask
PeriodicTask.objects.update(last_run_at=None)
