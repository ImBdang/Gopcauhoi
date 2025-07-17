import zlib
import json
from datetime import datetime


def calculate_crc32(input_string: str) -> str:
    crc_value = zlib.crc32(input_string.encode('utf-8')) & 0xFFFFFFFF
    return f"{crc_value:08X}"

def get_formatted_date_time_for_signature(dt_object: datetime = None) -> str:
    if dt_object is None:
        dt_object = datetime.now() 
    return dt_object.strftime("%Y-%m-%d %H:%M:00")

def generate_x_request_signature(
    request_method: str,
    request_body: dict,
    x_app_id: str,
    signature_datetime: datetime = None) -> str:
        body_string = ""
        if request_method.upper() in ["POST", "PUT"]:
            body_string = json.dumps(request_body, separators=(',', ':'))
        formatted_date_part = get_formatted_date_time_for_signature(signature_datetime)
        signature_input = body_string + x_app_id + formatted_date_part
        return calculate_crc32(signature_input)

def return_signature(method, body):

    X_APP_ID = "7040BD38-0D02-4CBE-8B0E-F4115C348003"
    REQUEST_DATA = {
        "method": method.upper(),
        "body": body
    }
    calculated_signature = generate_x_request_signature(
        request_method=REQUEST_DATA["method"],
        request_body=REQUEST_DATA["body"],
        x_app_id=X_APP_ID,
    )
    return calculated_signature



