import csv
import hashlib
from Models.Jobs import Jobs
import pandas as pd

def toHash(company: str, job_name: str, hr: str):
    rowString = company + job_name + hr
    hashed = hashlib.sha256(rowString.encode('utf-8'))
    return hashed.hexdigest()


def insertData():
    # url = Jobs.select().where(Jobs.url != '')
    with open('data_store/web_jobs.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'url':
                continue
            id_job = toHash(row[3], row[1], row[5])
            print(id_job)
            try:
                q = Jobs.insert(id_job=id_job, url=row[0], company_name=row[3], salary=row[2], scale=row[4],
                                job_name=row[1], hr=row[5], region=row[6])
                q.execute()
            except Exception as e:
                print('数据重复，跳过存储', e)
                pass


def selectData():
    # query = (Jobs.select(Jobs.url)
    #      .where(Jobs.id_job=='00269bdfa4461f06f875829cc2cb8c11fd617960b9be9a30068e206aa68579eb'))
    # q=Jobs.get_by_id(Jobs.id_job=='00269bdfa4461f06f875829cc2cb8c11fd617960b9be9a30068e206aa68579eb')
    # query = q

    query = (Jobs.select(Jobs.url, Jobs.chated, Jobs.id_job, Jobs.job_name)
             .where((Jobs.scale.not_in(['20-99人', '0-20人'])) &
                    ((Jobs.job_name.contains('web')) | (Jobs.job_name.contains('前端'))) & (
                            Jobs.salary.regexp('^[0-2][^-]') | Jobs.salary.regexp('^[7-9][-]')) & (Jobs.chated==0))
             )
    query = query.execute()
    c = 0
    for i in query:
        c = c+1
        print(c)


def output_data():
    query = (Jobs.select(Jobs.url, Jobs.chated, Jobs.id_job, Jobs.job_name, Jobs.active, Jobs.hr, Jobs.scale ,Jobs.company_name, Jobs.salary)
             .where(((Jobs.job_name.contains('web')) | (Jobs.job_name.contains('前端'))) & (
                            Jobs.salary.regexp('^[1-2][0-4]')) & Jobs.active == 1)

             )
    query = query.execute()
    exl = {'job_name':[], 'url':[], 'company':[], 'salary':[], 'scale':[]}
    for i in query:
        exl['job_name'].append(i.job_name)
        exl['url'].append(i.url)
        exl['company'].append(i.company_name)
        exl['salary'].append(i.salary)
        exl['scale'].append(i.scale)
    df = pd.DataFrame(exl)
    print(df)
    df.to_excel('web_jobs.xlsx', index=False, engine='openpyxl')



# selectData()
insertData()
# output_data()