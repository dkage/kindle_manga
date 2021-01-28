from core.models import SystemLog, User


def log_basic_entry(request, operation):

    logger = SystemLog()
    logger.operation = operation
    user = User.objects.get(id=request.user.id)
    logger.triggered_by = user
    logger.save()


def log_full_scan_query():
    try:
        system_log = SystemLog.objects.filter(operation='Full Scan').order_by('-date')[0]
    except IndexError:
        system_log = dict()
        system_log['triggered_by'] = 'Not done yet'
        system_log['date'] = ''

    return system_log
