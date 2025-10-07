from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout


class AdminIdleTimeoutMiddleware(MiddlewareMixin):
    """Logs out staff users from the admin after 90s of inactivity.
    Stores last activity in session under 'admin_last_activity'.
    """

    IDLE_SECONDS = 90

    def process_request(self, request):
        if request.path.startswith('/admin'):
            now = datetime.utcnow()
            last_activity_ts = request.session.get('admin_last_activity')
            if last_activity_ts:
                try:
                    last_activity = datetime.fromisoformat(last_activity_ts)
                except Exception:
                    last_activity = None
                if last_activity:
                    delta = (now - last_activity).total_seconds()
                    if delta > self.IDLE_SECONDS and request.user.is_authenticated:
                        # Force logout and redirect to admin login
                        logout(request)
                        return redirect('admin:login')
            # update timestamp
            request.session['admin_last_activity'] = now.isoformat()
        return None
