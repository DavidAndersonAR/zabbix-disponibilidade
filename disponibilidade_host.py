from pyzabbix import ZabbixAPI
from datetime import datetime, timedelta
import time
import pymysql



hosts_zabbix=[]
data_selecionada = 5

def dispo_host():
    try:
        zapi = ZabbixAPI("seu_servidor_zabbix")
        zapi.login("user", "senha")

        print(f"Login feito com sucesso! {zapi.api_version()}")
    except Exception as erro:
        print(erro)



    #data desejada
    #inicio="13/06/2022 10:00:00"
    inicio=(datetime.now() - timedelta(days=data_selecionada)).strftime("%d/%m/%Y")
    print(inicio)
    #fim="19/12/2018 00:00:00"
    fim=datetime.now().strftime("%d/%m/%Y")

    #horario timestamp
    data_inicio=time.mktime(datetime.strptime(inicio, "%d/%m/%Y").timetuple())
    data_fim=time.mktime(datetime.strptime(fim, "%d/%m/%Y").timetuple())
 
    grupo = 289

    hosts = zapi.host.get(output=["hostid","name"],selectGroups="extend", selectTags="extend", groupids=grupo, selectInterfaces="extend")
    #print(hosts)
    for teste in hosts:
        testenome = teste["name"]
        id_testenome=teste["hostid"]
        interface_teste = zapi.hostinterface.get(hostids=id_testenome, filter={"type" : 2})
        for host in interface_teste:
            host_ativo = host['hostid']

            item = zapi.item.get(search={"key_": "icmpping"}, output="itemid", hostids=host_ativo)
            #DISPONIBILIDADE
            if len(item) > 0:
                item_id= item[0]["itemid"]
                history = zapi.history.get(itemids=item_id, time_from=int(data_inicio), time_till=int(data_fim))
                quantidade_history = len(history)
                contador = 0
                dispo = 000

                if quantidade_history > 0:
                    for y in range(0, quantidade_history):
                        if history[y]["value"] == "1":
                            contador = contador + 1

                    if quantidade_history > 0:
                        dispo = (contador / (quantidade_history)) * 100
                        primeiros_digitos = '{:.2f}'.format(dispo).replace('.', ',')
                     




                    hosts_zabbix.append({
                            
                            'availability_formatada' : primeiros_digitos,
                            'ID' : id_testenome,
                            'Disponibilidade' : primeiros_digitos,
                            'host' : testenome
                            
                        })

                print(f"{testenome}, {id_testenome} - {primeiros_digitos} ")

