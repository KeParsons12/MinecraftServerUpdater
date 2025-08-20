import requests, shutil, datetime, os, subprocess, time, platform, asyncio

def readConfig():
    print('Reading config...')
    if os.path.exists('.config'):
        config = {}
        with open('.config', 'r') as configFile:
            for line in configFile:
                if line.startswith('#'):
                    config[line] = ''
                else:
                    key, value = line.partition('=')[::2]
                    if key == 'server-directory':
                        config[key.strip()] = value.strip().replace('\\', '/')
                    else:
                        config[key.strip()] = value.strip()
        # print(config)
    else:
        config = {'# Minecraft Server Updater config file created ' + datetime.datetime.now().strftime('%m/%d/%Y %I:%M%p') + '\n' : '', 'simulation-distance': '10', 'view-distance': '10', '# Note RAM 1024 = 1GB, 2048 = 2GB, 4086 = 4GB, 8162 = 8GB, etc...\n' : '','dedicated-ram': '1024', 'server-directory' : os.path.abspath(os.path.curdir).replace("\\", "/") + '/minecraftserver'}
        with open('.config', 'w') as configFile:
            for key in config:
                if key.startswith('#'):
                    configFile.write(key)
                else:
                    configFile.write(f'{key}={config[key]}\n')
    return config

def writeConfig():
    print('Writing config files...')
    # Write config file
    # print(config)
    with open('.config', 'w') as configFile:
        for key in config:
            if key.startswith('#'):
                configFile.write(key)
            else:
                configFile.write(f'{key}={config[key]}\n')

    # Read properties file
    with open(config['server-directory'] + '/server.properties', 'r') as propsFile:
        lines = propsFile.readlines()
        for id, line in enumerate(lines):
            for key in config:
                if line.startswith(key):
                    lines[id] = f'{key}={config[key]}\n'

    # Write properties file
    with open(config['server-directory'] + '/server.properties', 'w') as propsFile:
        # print(lines)
        propsFile.writelines(lines)

def checkEula():
    print('Checking Eula...')
    with open(config['server-directory'] + '/eula.txt', 'r') as eula:
        lines = eula.readlines()
        for id, line in enumerate(lines):
            if line.startswith('eula='):
                lineNum = id
                key, value = line.partition('=')[::2]
                value.strip()

    if value == 'false\n':
        line = 'eula=true\n'
        lines[lineNum] = line 
        print('Writing to eula...')
        with open(config['server-directory'] + '/eula.txt', 'w') as eula:
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
                if os.path.exists(config['server-directory']) == False:
                    os.mkdir(config['server-directory'])
                open(config['server-directory'] + '/server.jar', 'wb').write(requests.get(serverUrl).content)
                print('Download complete.')

async def startServer(firstRun=False):
    print('Starting server...')
    os.chdir(config['server-directory'])
    if osName == 'Linux':
        cmd = await asyncio.create_subprocess_shell('java ' + '-Xms1024M -Xmx' + config['dedicated-ram'] + 'M ' + '-jar ' + config['server-directory'] + '/server.jar --nogui', creationflags=subprocess.CREATE_NEW_CONSOLE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    elif osName == 'Windows':
        cmd = await asyncio.create_subprocess_shell('java ' + '-Xms1024M -Xmx' + config['dedicated-ram'] + 'M ' + '-jar ' + config['server-directory'] + '/server.jar --nogui', creationflags=subprocess.CREATE_NEW_CONSOLE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        if firstRun:
            while os.path.exists(config['server-directory'] + '/eula.txt') == False:
                cmd.communicate()
                time.sleep(5)
            time.sleep(10)
            cmd.terminate()
            cmd.wait()
    os.chdir(currentDirectory)
    return cmd

async def printCmdOutput(cmd):
    return await cmd.stdout.readline()

# async def startServer(firstRun=False):
#     print('Starting server...')
#     os.chdir(config['server-directory'])
#     if osName == 'Linux':
#         cmd = await asyncio.create_subprocess_shell('java ' + '-Xms1024M -Xmx' + config['dedicated-ram'] + 'M ' + '-jar ' + config['server-directory'] + '/server.jar --nogui', creationflags=asyncio.subprocess.CREATE_NEW_CONSOLE, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)
#     elif osName == 'Windows':
#         cmd = await asyncio.create_subprocess_shell('java ' + '-Xms1024M -Xmx' + config['dedicated-ram'] + 'M ' + '-jar ' + config['server-directory'] + '/server.jar --nogui', stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)
        
#     if firstRun:
#         while os.path.exists(config['server-directory'] + '/eula.txt') == False:
#             # cmd.communicate()
#             time.sleep(5)
#         time.sleep(10)
#         cmd.terminate()
#         cmd.wait()
#     os.chdir(currentDirectory)
#     return cmd

def backupSever():
    print('Backing up server...')
    if os.path.exists(config['server-directory']):

    # Create backup of server folder
        shutil.copytree(config['server-directory'], config['server-directory'] + datetime.date.today().strftime("%Y%m%d"), dirs_exist_ok=True)

    else:
        raise FileNotFoundError(f"Backup failed: No such directory. {config['server-directory']}") 
    return

osName = platform.system()
currentDirectory = os.path.abspath(os.path.curdir)

# Read config file or create one with default values if one does not exist.
config = readConfig()

async def main():
    try:

        # Read Eula file and mark true if exists. If not start server to generate eula.
        if os.path.exists(config['server-directory'] + '/eula.txt') & os.path.exists(config['server-directory'] + '/server.jar'):
            checkEula()
            writeConfig()

        elif os.path.exists(config['server-directory'] + '/server.jar'):
            await startServer(True)
            writeConfig()
            checkEula()

        else:
            downloadLatestServer()
            await startServer(True)
            writeConfig()
            checkEula()

        gameWindow = await startServer()

        gameWindowPrinter = asyncio.create_task(gameWindow.stdout.readline())

        while True:
            if gameWindowPrinter.done():
                print(gameWindowPrinter.result())
                gameWindowPrinter = asyncio.create_task(printCmdOutput(gameWindow))
            #await asyncio.sleep(0.1)
            await print('Weeeee')





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
        # gameWindow.stdout.flush()
        # time.sleep(25)
        # stopcmd = '/stop\n'
        # gameWindow.stdin.write(stopcmd.encode("utf-8"))
        # gameWindow.stdin.flush()
        # supercool = gameWindow.stdout.readlines()
        # print(supercool)
        print('script finished')
        exit(0)

    except Exception as e:
        print(e)
        exit(1)

asyncio.run(main())

# try:
#     # Get status of minecraft server
#     response = requests.get('https://api.mcstatus.io/v2/status/java/kurtisparsons.com')
#     print('Server status response code:', response.status_code)
#     if response.status_code == 200:

#         responseJson = response.json()

#         serverVersion = responseJson['version']['name_raw']
#         playerCount = responseJson['players']['online']

#         if playerCount == 0:
#             # Get latest version number
#             response = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json')
#             print('Version manifest response code:', response.status_code)
#             if response.status_code == 200:
#                 responseJson = response.json()

#                 latestVersion = responseJson['latest']['release']

#                 # print(len(responseJson['versions']))

#                 if serverVersion != latestVersion:
#                     for versions in responseJson['versions']:
#                         if versions['id'] == latestVersion:
#                             # print(versions['url'])
#                             # Get Url to download the latest server .jar file
#                             response = requests.get(versions['url'])
#                             print('download link response code:', response.status_code)
#                             if response.status_code == 200:
#                                 responseJson = response.json()
#                                 serverUrl = responseJson['downloads']['server']['url']
#                                 # print(serverUrl)
#                                 # Download latest .jar file
#                                 open(currentDirectory + '/server.jar', 'wb').write(requests.get(serverUrl).content)
#                                 print('Download complete.')

#                                 # Bash Commands (stop server process) (wait for process to stop)
#                                 bashResult = subprocess.run("systemctl stop minecraft-server.service", shell=True, capture_output=True, text=True)
#                                 print(bashResult)
#                                 time.sleep(30)

#                                 # Copy server folder
#                                 if os.path.exists(serverDirectory):
#                                     # print(serverDirectory, datetime.date.today())
#                                     # Create backup of server folder
#                                     shutil.copytree(serverDirectory, serverDirectory + datetime.date.today().strftime("%Y%m%d"), dirs_exist_ok=True)
                                    
#                                     # Move new server file into existing directory
#                                     shutil.copy(currentDirectory + '/server.jar', serverDirectory)

#                                     # Bash commands (start server process)
#                                     bashResult = subprocess.run("systemctl start minecraft-server.service", shell=True, capture_output=True, text=True)
#                                     print(bashResult)
#                                     open(logFilePath, 'a').write(f'{datetime.datetime.now()}: Server succesfully updated to version: {latestVersion}\n')
                                    
#                                 else:
#                                     print('Server directory does not exist.')
#                                     open(logFilePath, 'a').write(f'{datetime.datetime.now()}: Server directory does not exist.\n')                               

#                 else:
#                     print(f'Server is up to date. Version: {serverVersion}')
#                     open(logFilePath, 'a').write(f'{datetime.datetime.now()}: Server is up to date. Version: {serverVersion}.\n')

#         else:
#             print('Server not empty.', playerCount, 'players in game.')
#             open(logFilePath, 'a').write(f'{datetime.datetime.now()}: Server not empty. {playerCount} players in game.\n')


# except Exception as e:
#     print('Unspecified Error')
#     print(e)
#     open(logFilePath, 'a').write(f'{datetime.datetime.now()}: ERROR: {e}\n')
