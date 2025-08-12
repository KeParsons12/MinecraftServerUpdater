import requests, shutil, datetime, os, subprocess, time

serverDirectory = "/home/kupar/gameservers/minecraft"
currentDirectory = "/home/kupar/gameservers"
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
