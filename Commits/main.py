# coding=utf-8
from datetime import datetime, timedelta


def datetime_parser(line):
    date_str = ','.join(line.split(' ')[2:5])
    date = datetime.strptime(date_str[:19], '%Y-%m-%d,%H:%M:%S')
    if date_str[20] == '+':
        date -= timedelta(hours=int(date_str[21:23]), minutes=int(date_str[23:]))
    elif date_str[20] == '-':
        date += timedelta(hours=int(date_str[21:23]), minutes=int(date_str[23:]))
    return date


def add_user_commits_by_year(year, committer):
    if year in result[committer]['commits_by_years'].keys():
        result[committer]['commits_by_years'][year] += 1
    else:
        result[committer]['commits_by_years'][year] = 1


def add_statistic_by_year(year):
    if year in statistic_by_year.keys():
        statistic_by_year[year] += 1
    else:
        statistic_by_year[year] = 1


def add_user_total_commits(committer):
    if committer in result.keys():
        result[committer]['user_total_commits'] += 1
    else:
        result[committer] = {'user_total_commits': 1}
        result[committer]['commits_by_years'] = {}
        result[committer]['percentage_per_year'] = {}


def add_statistic_and_user_commits_for_3_months(committer, date):
    if committer not in statistic_by_3_month.keys():
        statistic_by_3_month[committer] = {'start_time': date}
        result[committer]['commits_for_3_months'] = 0
    elif committer in statistic_by_3_month.keys() and statistic_by_3_month[committer]['start_time'] - date < timedelta(
            days=90):
        result[committer]['commits_for_3_months'] += 1
        statistic_by_3_month['total_commits_for_3_months'] += 1


def percentage_calculation(result):
    for committer, value in result.items():
        percentage_value = float(value['user_total_commits']) / total_records * 100
        result[committer]['percentage_of_all_commits'] = round(percentage_value, 2)
        percentage_of_quantity_for_3_months_value = float(result[committer]['commits_for_3_months']) / \
                                                    statistic_by_3_month['total_commits_for_3_months'] * 100
        result[committer]['percentage_of_commits_for_3_months'] = round(percentage_of_quantity_for_3_months_value, 2)
        for year, value in result[committer]['commits_by_years'].items():
            percentage_per_year = float(value) / statistic_by_year[year] * 100
            result[committer]['percentage_per_year'][year] = round(percentage_per_year, 2)


def show_and_write_result(result):
    result_file = open('Result.txt', 'w+')
    labels = ['Пользователь: ', 'Кол-во коммитов пользователя: ', 'Процент от общего кол-ва коммитов: ',
              'Кол-во коммитов по годам: ', 'Процент от общего кол-ва коммитов за год: ',
              'Кол-во коммитов за последние 3 месяца: ', 'Процент от общего числа коммитов за последние 3 месяца: ']
    for committer in result.keys():
        print labels[0] + committer
        result_file.write(labels[0] + committer + '\n')
        user_total_commits = str(result[committer]['user_total_commits'])
        print labels[1] + user_total_commits
        result_file.write(labels[1] + user_total_commits + '\n')
        percentage_of_all_commits = str(result[committer]['percentage_of_all_commits'])
        print labels[2] + percentage_of_all_commits
        result_file.write(labels[2] + percentage_of_all_commits + '\n')
        print labels[3]
        result_file.write(labels[3] + '\n')
        for year, value in result[committer]['commits_by_years'].items():
            print '{}:{}'.format(year, value)
            result_file.write('{}:{}'.format(year, value) + '\n')
        print labels[4]
        result_file.write(labels[4] + '\n')
        for year, value in result[committer]['percentage_per_year'].items():
            print '{}:{}'.format(year, value)
            result_file.write('{}:{}'.format(year, value) + '\n')
        commits_for_3_months = str(result[committer]['commits_for_3_months'])
        print labels[5] + commits_for_3_months
        result_file.write(labels[5] + commits_for_3_months + '\n')
        percentage_of_commits_for_3_months = str(result[committer]['percentage_of_commits_for_3_months'])
        print labels[6] + percentage_of_commits_for_3_months
        result_file.write(labels[6] + percentage_of_commits_for_3_months + '\n')
    result_file.close()


path = raw_input('Введите путь до файла: ')
log = open(path)

result = {}
total_records = 0
statistic_by_year = {}
committer = ''
statistic_by_3_month = {'total_commits_for_3_months': 0}

for line in log:
    if 'committer' in line:
        total_records = total_records + 1
        committer = line.split(' ')[1].rstrip()
        add_user_total_commits(committer)
    if 'timestamp' in line:
        date = datetime_parser(line)
        year = date.year
        add_statistic_and_user_commits_for_3_months(committer, date)
        add_statistic_by_year(year)
        add_user_commits_by_year(year, committer)

log.close()
percentage_calculation(result)
show_and_write_result(result)
