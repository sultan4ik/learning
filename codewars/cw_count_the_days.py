import datetime


def count_days(d):
    current = datetime.datetime.today()
    result = current.date() - d.date()
    if result.days == 0:
        return "Today is the day!"
    elif result.days > 0:
        return "The day is in the past!"
    else:
        if (d - current).seconds // 3600 >= 12:
            return f'{(d - current).days + 1} days'
        else:
            return f'{(d - current).days} days'


def main():
    pass


if __name__ == '__main':
    main()
