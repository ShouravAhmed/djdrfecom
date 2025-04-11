import logging
import random
from datetime import datetime, timedelta

from django.core.cache import cache
from rest_framework import status

from common.utils import is_vaid_phone_number

logger = logging.getLogger('main')


def sms_otp(otp):
    logger.info(f"SMS OTP: {otp}")


def send_login_otp(phone_number):
    if not is_vaid_phone_number(phone_number):
        return {'message': 'Please Enter A Correct Phone Number.', 'status': 'error'}

    otp = str(random.randint(100000, 999999))
    otp_cache_key = f'OTP_{phone_number}'
    otp_req_cnt_key = f'OTP_REQ_CNT_{phone_number}'
    otp_req_timeout_key = f'OTP_REQ_TIMEOUT_{phone_number}'

    otp_req_cnt = cache.get(otp_req_cnt_key) or 0

    if otp_req_cnt >= 5:
        return {'message': f'An OTP has already been sent to {phone_number}.\nCan\'t resend OTP more then 5 times a day.', 'status': 'OK'}

    otp_req_timeout = cache.ttl(otp_req_timeout_key)
    if otp_req_timeout > 0:
        timeout_str = ""
        if otp_req_timeout <= 60:
            timeout_str = f'{otp_req_timeout} Seconds'
        else:
            otp_req_timeout = otp_req_timeout / 60
            if otp_req_timeout <= 60:
                timeout_str = f'{int(otp_req_timeout)} Minute {int((otp_req_timeout - int(otp_req_timeout)) * 60)} Seconds'

        return {'message': f'An OTP has already been sent to {phone_number}.\nCan\'t resend OTP before {timeout_str}.', 'status': 'OK', 'count': otp_req_cnt}

    cache.set(otp_cache_key, otp, None)
    cache.expire_at(otp_cache_key, datetime.now() + timedelta(days=30))

    cache.set(otp_req_timeout_key, 0, None)
    cache.expire_at(otp_req_timeout_key, datetime.now() +
                    timedelta(minutes=(3**otp_req_cnt)))

    otp_req_cnt = otp_req_cnt + 1
    cache.set(otp_req_cnt_key, otp_req_cnt, None)
    cache.expire_at(otp_req_cnt_key, datetime.now() +
                    timedelta(days=1))

    sms_otp(otp)
    return {'message': f'An OTP has been sent to your phone number {phone_number}', 'status': 'OK'}
