import requests, shutil, datetime, os, subprocess, time, platform

def checkEula():
    print('Checking Eula...')
    with open(config['server directory'] + '/eula.txt', 'r') as eula:
        lines = eula.readlines()
        for id, line in enumerate(lines):
            if line.startswith('eula='):
                lineNum = id
                key, value = line.partition('=')[::2]
                value.strip()

    if value == 'false\n':
        line = 'eula=true\n'
        lines[lineNum] = line 
        print('writing to eula...')
        with open(config['server directory'] + '/eula.txt', 'w') as eula:
            print(lines)
            eula.writelines(lines)

def downloadLatestServer():
    response = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json')
    print('Version manifest response code:', response.status_code)
    if response.status_code == 200:
        responseJson = response.json()

        latestVersion = responseJson['latest']['release']

    for versions in responseJson['versions']:
        if versions['id'] == latestVersion:
            # print(versions['url'])
            # Get Url to download the latest server .jar file
            response = requests.get(versions['url'])
            print('download link response code:', response.status_code)
            if response.status_code == 200:
                responseJson = response.json()
                serverUrl = responseJson['downloads']['server']['url']
                # print(serverUrl)
                # Download latest .jar file
                if os.path.exists(config['server directory']) == False:
                    os.mkdir(config['server directory'])
                open(config['server directory'] + '/server.jar', 'wb').write(requests.get(serverUrl).content)
                print('Download complete.')

def startServer(firstRun=False):
    print('Starting server...')
    os.chdir(config['server directory'])
    if osName == 'Linux':
        cmd = subprocess.Popen('java -jar ' + config['server directory'] + '/server.jar --nogui')
    elif osName == 'Windows':
        cmd = subprocess.Popen('java -jar ' + config['server directory'] + '/server.jar --nogui')
        if firstRun:
            time.sleep(20)
            cmd.terminate()
            cmd.wait()
    os.chdir(currentDirectory)

osName = platform.system()
currentDirectory = os.path.curdir

# Read config file or create one with default values if one does not exist.
if os.path.exists('.config'):
    config = {}
    with open('.config', 'r') as configFile:
        for line in configFile:
            key, value = line.partition('=')[::2]
            if key == 'server directory':
                config[key.strip()] = value.strip().replace('\\', '/')
            else:
                config[key.strip()] = value.strip()
    print(config)
else:
    config = {'port': '25565', 'dedicated ram': '4gb', 'server directory' : os.path.abspath(os.path.curdir).replace("\\", "/") + '/minecraftserver'}
    with open('.config', 'w') as configFile:
        for key in config:
            configFile.write(f'{key}={config[key]}\n')

# Read Eula file and mark true if exists. If not start server to generate eula.
if os.path.exists(config['server directory'] + '/eula.txt'):
    checkEula()
    startServer()

elif os.path.exists(config['server directory'] + '/server.jar'):
    startServer(True)
    checkEula()
    startServer()

else:
    downloadLatestServer()
    startServer(True)
    checkEula()
    startServer()



serverDirectory = "/home/kupar/gameservers/minecraft"
# currentDirectory = "/home/kupar/gameservers"
logFilePath = "/home/kupar/gameservers/log.txt"
# currentTime = datetime.datetime.now()   
# laterTime = currentTime + datetime.timedelta(hours = 1)
# laterTimeSecond = currentTime + datetime.timedelta(seconds = 1)

# while True:
    # while currentTime < laterTime:
    #     currentTime = datetime.datetime.now()
        
        # if currentTime >= laterTimeSecond:
        #     print(currentTime)
        #     laterTimeSecond = currentTime + datetime.timedelta(seconds = 1)


# laterTime = currentTime + datetime.timedelta(hours = 1)
print('script finished')
exit(0)
try:
    # Get status of minecraft server
    response = requests.get('https://api.mcstatus.io/v2/status/java/kurtisparsons.com')
    print('Server status response code:', response.status_code)
    if response.status_code == 200:

        responseJson = response.json()

        serverVersion = responseJson['version']['name_raw']
        playerCount = responseJson['players']['online']

        if playerCount == 0:
            # Get latest version number
            response = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json')
            print('Version manifest response code:', response.status_code)
            if response.status_code == 200:
                responseJson = response.json()

                latestVersion = responseJson['latest']['release']

                # print(len(responseJson['versions']))

                if serverVersion != latestVersion:
                    for versions in responseJson['versions']:
                        if versions['id'] == latestVersion:
                            # print(versions['url'])
                            # Get Url to download the latest server .jar file
                            response = requests.get(versions['url'])
                            print('download link response code:', response.status_code)
                            if response.status_code == 200:
                                responseJson = response.json()
                                serverUrl = responseJson['downloads']['server']['url']
                                # print(serverUrl)
                                # Download latest .jar file
                                open(currentDirectory + '/server.jar', 'wb').write(requests.get(serverUrl).content)
                                print('Download complete.')

                                # Bash Commands (stop server process) (wait for process to stop)
                                bashResult = subprocess.run("systemctl stop minecraft-server.service", shell=True, capture_output=True, text=True)
                                print(bashResult)
                                time.sleep(30)

                                # Copy server folder
                                if os.path.exists(serverDirectory):
                                    # print(serverDirectory, datetime.date.today())
                                    # Create backup of server folder
                                    shutil.copytree(serverDirectory, serverDirectory + datetime.date.today().strftime("%Y%m%d"), dirs_exist_ok=True)
                                    
                                    # Move new server file into existing directory
                                    shutil.copy(currentDirectory + '/server.jar', serverDirectory)

                                    # Bash commands (start server process)
                                    bashResult = subprocess.run("systemctl start minecraft-server.service", shell=True, capture_output=True, text=True)
                                    print(bashResult)
                                    open(logFilePath, 'a').write(f'{datetime.datetime.now()}: Server succesfully updated to version: {latestVersion}\n')
                                    
                                else:
                                    print('Server directory does not exist.')
                                    open(logFilePath, 'a').write(f'{datetime.datetime.now()}: Server directory does not exist.\n')                               

                else:
                    print(f'Server is up to date. Version: {serverVersion}')
                    open(logFilePath, 'a').write(f'{datetime.datetime.now()}: Server is up to date. Version: {serverVersion}.\n')

        else:
            print('Server not empty.', playerCount, 'players in game.')
            open(logFilePath, 'a').write(f'{datetime.datetime.now()}: Server not empty. {playerCount} players in game.\n')


except Exception as e:
    print('Unspecified Error')
    print(e)
    open(logFilePath, 'a').write(f'{datetime.datetime.now()}: ERROR: {e}\n')
