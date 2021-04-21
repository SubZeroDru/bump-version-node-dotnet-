import subprocess
import os
import fnmatch


latestCommit = (subprocess.check_output("git rev-parse --short HEAD", shell=True).strip()).decode("utf-8")
changedFiles = (subprocess.check_output("git diff-tree --no-commit-id --name-only -r " + latestCommit, shell=True)
                ).decode().split('\n')
services = {}
fileNamePattern = "*.csproj"


def getFilesByPattern(rootDir, fileNamePattern):
    listOfitems = os.listdir(rootDir)
    files = list()
    for item in listOfitems:
        fullPath = os.path.join(rootDir, item)
        if os.path.isdir(fullPath):
            files = files + getFilesByPattern(fullPath, fileNamePattern)
        elif fnmatch.fnmatch(item, fileNamePattern):
            files.append(fullPath)
    return files


for x in changedFiles:
    arr = x.split("/")
    if len(arr) >= 2:
        name = arr[1]
        services[name] = name
    print(x)
for service in services:
    path = "./services/" + service
    print('updating' + path)
    if os.path.exists(path + "/package.json"):
        print('package.json')
        subprocess.call('cd ' + path + ' && npm version patch', shell=True)
    else:
        try:
            csprojs = getFilesByPattern('./services/' + service, fileNamePattern)
            for csproj in csprojs:
                subprocess.call(' dotnet version -f ' + csproj + ' --skip-vcs patch', shell=True)
        except:
            print("csproj is not found")
