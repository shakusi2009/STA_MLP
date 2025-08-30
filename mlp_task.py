from __future__ import print_function
import volcenginesdkmlplatform20240701

import volcenginesdkcore
from pprint import pprint

from volcenginesdkcore.rest import ApiException
import time_utils

import pandas as pd
from datetime import datetime
import configparser

from tools_utils import divide_ceil

# 全局变量
global_jobs_data = []
global_pageid = 1

def getListResource():
    # ListResourceGroupsRequest
    # use global default configuration
    api_instance = volcenginesdkmlplatform20240701.MLPLATFORM20240701Api()
    # use custom configuration
    request = volcenginesdkmlplatform20240701.ListResourceGroupsRequest()

    try:
        resp = api_instance.list_resource_groups(request)
        pprint(resp)
    except ApiException as e:
        print("Exception when calling MLPLATFORM20240701Api->list_resource_groups: %s\n" % e)

def loopJobs(resp) -> object:
    # 提取所需字段
    jobs_data = []
    roles_data = []
    if hasattr(resp, 'items'):
        for job in resp.items:
            job_info = {
                '任务创建人': getattr(job, 'created_by', 'default:root').split(':')[-1],
                '任务名称': getattr(job, 'name', None),
                '任务创建时间': time_utils.time_convert(getattr(job, 'create_time', None)),
                '最大运行时常(小时)': getattr(getattr(job, 'resource_config', None), 'max_runtime_seconds',
                                              None) / 3600 if hasattr(job, 'resource_config') else None,
                '资源信息': [],
                '任务状态': getattr(getattr(job, 'status', None), 'state', None)
            }
            # 提取roles中的instance_type_id
            if hasattr(job.resource_config, 'roles') and job.resource_config.roles:

                for role in job.resource_config.roles:
                    if role.resource.instance_type_id != "":
                        role_info = {}
                        role_info['name'] = role.name
                        role_info['资源数量'] = role.replicas
                        role_info['资源配置'] = role.resource.instance_type_id
                        job_info['资源信息'].append(role_info)
            else:
                job_info['资源信息'] = None
            jobs_data.append(job_info)
            global_jobs_data.append(job_info)

    pprint(resp)

def getListJobs(pageid = 1) -> object:
    api_instance = volcenginesdkmlplatform20240701.MLPLATFORM20240701Api()

    request = volcenginesdkmlplatform20240701.ListJobsRequest(
       page_number=pageid
    );
    try:
        resp = api_instance.list_jobs(request)
        global global_pageid
        loopJobs(resp)
        if pageid < divide_ceil(resp.total_count):
            global_pageid += 1
            getListJobs(global_pageid)
        else:
            # 创建DataFrame并保存到Excel
            df = pd.DataFrame(global_jobs_data)
            excel_file = f'./result/jobs_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            df.to_excel(excel_file, index=False)
            print(f'数据已保存到: {excel_file}')

    except ApiException as e:
        print("获取自定义任务列表失败：%s\n" % e)

if __name__ == '__main__':
    """读取INI格式的配置文件"""
    # 创建配置解析器
    config = configparser.ConfigParser()

    # 读取配置文件
    # 请在cfg.ini中配置对MLP平台有权限的账号AK/SK
    config.read("config/cfg.ini", encoding='utf-8')

    vol_ak = ""
    vol_sk = ""
    # 获取所有section
    sections = config.sections()

    if 'volcengine' in sections:
        vol_ak = config.get('volcengine', 'ak')
        vol_sk = config.get('volcengine', 'sk')

    configuration = volcenginesdkcore.Configuration()
    configuration.ak = vol_ak
    configuration.sk = vol_sk


    configuration.region = "cn-shanghai"
    # configuration.region = "cn-beijing"

    configuration.client_side_validation = False
    # set default configuration
    volcenginesdkcore.Configuration.set_default(configuration)

    # 获取资源组列表
    # getListResource();

    # 获取自定义任务列表
    getListJobs()
