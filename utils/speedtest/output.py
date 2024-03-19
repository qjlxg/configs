import json
import base64
import os
import time
import requests

out_json = './out.json'

sub_all_base64 = "./sub/sub_merge_base64.txt"
sub_all = "./sub/sub_merge.txt"
Eternity_file_base64 = "./Eternity"
Eternity_file = "./Eternity.txt"
Eternity_Base = "./EternityBase"

splitted_output = "./sub/splitted/"


def read_json(file):  # 将 out.json 内容读取为列表
    while os.path.isfile(file) == False:
        # log
        #file_list = os.listdir("./")
        #print(file_list)
        print('Awaiting speedtest complete')
        time.sleep(30)
    with open(file, 'r', encoding='utf-8') as f:
        print('Reading out.json')
        proxies_all = json.load(f)["nodes"]
        f.close()
    return proxies_all


def output(list, num):
    # Sort based on avg speed rather than max speed
    list = sorted(list, key=lambda x: x['avg_speed'], reverse=True)

    # Protocol distribution analysis
    protocol_counts = {'vmess': 0, 'trojan': 0, 'ss': 0}
    for item in list[:num]:  # Analyze only the top 'num'
        if item['protocol'] == 'vmess':
            protocol_counts['vmess'] += 1
        elif item['protocol'] == 'trojan':
            protocol_counts['trojan'] += 1
        else:  # Assuming the rest are 'ss' for this example
            protocol_counts['ss'] += 1

    print("Protocol Distribution (Top %d):" % num, protocol_counts)

    # Target distribution
    desired_distribution = {
        'vmess': 0.6,  # 60% vmess
        'trojan': 0.2,  # 20% trojan
        'ss': 0.2       # 20% ss
    }

    # Calculate replacements needed
    ss_to_replace = max(0, protocol_counts['ss'] - int(num * desired_distribution['ss']))
    replacements_found = 0

    # Modified output list
    output_list = list[:num]

    # Replacement Logic
    i = num  # Start search index below top 'num'
    while replacements_found < ss_to_replace and i < len(list):
        if list[i]['protocol'] in ('vmess', 'trojan'):
            for j in range(num):
                if output_list[j]['protocol'] == 'ss':  # Find an ss to replace
                    output_list[j] = list[i]
                    replacements_found += 1
                    break  # Replace one ss at a time
        i += 1

    # Write LogInfo.txt
    output_list_info = []
    for item in output_list:
        info = "id: %s | remarks: %s | protocol: %s | ping: %s MS | avg_speed: %s MB | max_speed: %s MB | Link: %s\n" % (
            str(item["id"]), item["remarks"], item["protocol"], str(item["ping"]),
            str(round(item["avg_speed"] * 0.00000095367432, 3)), str(round(item["max_speed"] * 0.00000095367432, 3)),
            item["link"])
        output_list_info.append(info)
    with open('./LogInfo.txt', 'w') as f1:
        f1.writelines(output_list_info)
        print('Write Log Success!')

    output_list = []
    for index in range(list.__len__()):
        proxy = list[index]['link']
        output_list.append(proxy)

    # writing content as mixed and base64
    content = '\n'.join(output_list)
    content_base64 = base64.b64encode(
        '\n'.join(output_list).encode('utf-8')).decode('ascii')
    content_base64_part = base64.b64encode(
        '\n'.join(output_list[0:num]).encode('utf-8')).decode('ascii')

    # spliting different protocols
    os.makedirs(splitted_output, exist_ok=True)
    vmess_outputs = []
    trojan_outputs = []
    ssr_outputs = []
    ss_outputs = []

    for output in output_list:
        if str(output).startswith("vmess://"):
            vmess_outputs.append(output)
        if str(output).startswith("trojan://"):
            trojan_outputs.append(output)
        if str(output).startswith("ssr://"):
            ssr_outputs.append(output)
        if str(output).startswith("ss://"):
            ss_outputs.append(output)

    with open(splitted_output.__add__("vmess.txt"), 'w') as f:
        vmess_content = "\n".join(vmess_outputs)
        f.write(vmess_content)
        print('Write vmess splitted Success!')
        f.close()

    with open(splitted_output.__add__("trojan.txt"), 'w') as f:
        trojan_content = "\n".join(trojan_outputs)
        f.write(trojan_content)
        print('Write trojan splitted Success!')
        f.close()

    with open(splitted_output.__add__("ss.txt"), 'w') as f:
        ss_content = "\n".join(ss_outputs)
        f.write(ss_content)
        print('Write ss splitted Success!')
        f.close()

    ##################

    with open(sub_all_base64, 'w+', encoding='utf-8') as f:
        f.write(content_base64)
        print('Write All Base64 Success!')
        f.close()
    with open(Eternity_file_base64, 'w+', encoding='utf-8') as f:
        f.write(content_base64_part)
        print('Write Part Base64 Success!')
        f.close()

    with open(sub_all, 'w') as f:
        f.write(content)
        print('Write All Success!')
        f.close()
    with open(Eternity_Base, 'w') as f:
        f.write(content)
        print('Write Base Success!')
        f.close()
    with open(Eternity_file, 'w') as f:
        f.write('\n'.join(output_list[0:num]))
        print('Write Part Base Success!')
        f.close()
    return content


if __name__ == '__main__':
    num = 170
    value = read_json(out_json)
    output(value, value.__len__() if value.__len__() <= num else num)
