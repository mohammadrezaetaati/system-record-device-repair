import jdatetime
import datetime
from datetime import datetime as date


# Convert Gregorian date to Persian date
def g_to_p() -> str:

    date_Gregorian = date.now()
    date_persian = jdatetime.datetime.fromtimestamp(
        int(
            datetime.datetime.strptime(
                date_Gregorian.date().strftime("%Y-%m-%d"), "%Y-%m-%d"
            ).strftime("%s")
        )
    ).strftime("%Y-%m-%d")
    return date_persian


def create_work_order_number(work_order_number, date_string=g_to_p()) -> str:

    """
    Create a work order number for each device based on date,
    In such a way that it takes the year,
    month and then the number of device and creates an order number.
    For example:
    Date: 1401/05/06
    Number of device: 5
    Work order number: 14015/5
    If there is a work order number. One adds to the end of it.
    """

    if not work_order_number or int(date_string[:4]) > int(work_order_number[:4]):
        last_chr = 0
    else:
        last_chr = work_order_number[len(work_order_number) - 1:]
    last_chr = int(last_chr) + 1

    if int(date_string[5:7]) <= 9:
        return f"{date_string[:4]}{date_string[6]}/{last_chr}"
    else:
        return f"{date_string[:4]}{date_string[5:7]}/{last_chr}"
