from django_cron import CronJobBase, Schedule
from django.utils.timezone import now
from .models import MonthlyReport

class ResetMonthlyReportStatus(CronJobBase):
    
    RUN_AT_TIMES = ['00:00']  # Dijalankan pukul 00:00 setiap hari

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'app.reset_monthly_report_status'  

    def do(self):
        current_month = now().replace(day=1)
        MonthlyReport.objects.filter(report_month__lt=current_month).update(status='Belum Dicek')
        print(f"Status laporan berhasil di-reset pada {current_month}")
