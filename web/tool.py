from web.models import Sign

class MySign(Sign):
    time_diff = ''


def get_my_sign(signs):
    my_signs = []
    for sign in signs:
        my_sign = Sign()
        my_sign.id = sign.id
        my_sign.teacher = sign.teacher
        my_sign.student = sign.student
        my_sign.sign_in_time = sign.sign_in_time
        my_sign.sign_off_time = sign.sign_off_time
        my_sign.audit = sign.audit
        my_sign.remark = sign.remark
        my_signs.append(my_sign)

    return my_signs

def get_format_time(ts):
    ts = int(ts)
    second = ts % 60
    ts = ts / 60
    ts = int(ts)
    minute = ts % 60
    ts = ts / 60
    ts = int(ts)
    hour = ts
    ts = ''
    if hour < 10:
        time = '0' + str(hour) + ':'
    else:
        time = str(hour) + ':'

    if minute < 10:
        time = time + '0' + str(minute) + ':'
    else:
        time = time + str(minute) + ':'

    if second < 10:
        time = time + '0' + str(second)
    else:
        time += str(second)
    return time