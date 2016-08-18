#! /usr/bin/python
# -*- coding: utf-8 -*-
# Author: Floyda

import github3
import time as stime
import datetime
import random

DEBUG = True
MAX_RANGE = 10
gh = None


class Config:
    user_name = "<user_name>"
    user_passwd = "<user_passwd>"
    fake_repo_name = "fake-commit-log"



def debug_log(msg):
    print "[Info]", msg


def error_log(msg):
    print "[Error]", msg
    exit()

def get_github_date():
    us_time = datetime.datetime.utcnow()
    return str(us_time.date())


def has_commit_today():
    date = get_github_date()
    repos = github3.iter_user_repos(Config.user_name)
    try:
        for repo in repos:
            if date in str(repo.pushed_at):
                return True
    except:
        error_log("Cann't search User: %s" % Config.user_name)

    return False


def find_fake_repo(time=1):
    if time >= 10: return None
    try:
        global gh
        repo = gh.repository(Config.user_name, Config.fake_repo_name)
    except:
        debug_log("find_fake_repo ... %d" % time)
        return find_fake_repo(time + 1)
    return repo


def create_fake_repo(time=1):
    if time >= 10: return None
    try:
        repo = gh.create_repo(Config.fake_repo_name)
    except:
        debug_log("create_fake_repo ... %d" % time)
        return create_fake_repo(time + 1)
    return repo


def get_fake_repo():
    repo = find_fake_repo()
    if repo:
        return repo
    else:
        return create_fake_repo()


def fake_commit(time=1, failed_total=0):
    if failed_total > 12:
        error_log("Commit limit exceeded")
    if time == 0:
        debug_log("Fake Commit Finish")
        return

    repo = get_fake_repo()
    if repo is None:
        debug_log("Cann't get repository")
        fake_commit(time, failed_total + 1)

    timestamp = get_github_date() + "-" + str(datetime.datetime.utcnow().time())[:5]
    path = "log/%s" % timestamp
    msg = "hasnt commit at %s" % timestamp
    content = timestamp
    try:
        repo.create_file(path, msg, content)
    except:
        debug_log("... %d" % failed_total)
        stime.sleep(5)
        fake_commit(time, failed_total + 1)
        return

    debug_log("fake commit successful ... %d" % time)
    fake_commit(time - 1)


def main():
    debug_log(datetime.datetime.utcnow())
    debug_log("Fake Commit Began ...")
    global gh
    gh = github3.login(Config.user_name, password=Config.user_passwd)
    if DEBUG or not has_commit_today():
        fake_commit(random.randint(1, MAX_RANGE))
    else:
        debug_log('You has pushed today ...')


if __name__ == '__main__':
    main()
