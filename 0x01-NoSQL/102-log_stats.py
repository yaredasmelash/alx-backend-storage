#!/usr/bin/env python3
"""Log stats - new version"""
from pymongo import MongoClient


def logs(nginx):
    '''
    Prints Nginx request logs.
    '''
    print(f'{nginx.count_documents({})} logs')
    print('Methods:')
    reqs = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for req in reqs:
        print(f'\tmethod {req}: {nginx.count_documents({"method": req})}')
    print(f'{nginx.count_documents({"path": "/status"})} status check')


def ips(nginx):
    '''
    Prints he most present IPs in the collection
    '''
    print("IPs:")
    lists = nginx.aggregate(
            [
                {'$match': {}},
                {'$group': {
                    '_id': '$ip',
                    'tot': {'$sum': 1}
                }},
                {'$sort': {'tot': -1}},
                {'$limit': 10}
            ]
    )

    for li in lists:
        print(f'\t{li.get("_id")}: {li.get("tot")}')


def conn():
    '''
    Establish a connection with MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx
    logs(nginx)
    ips(nginx)


if __name__ == '__main__':
    conn()