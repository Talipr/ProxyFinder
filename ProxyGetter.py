import requests
from bs4 import BeautifulSoup
import socket

website_site = 'https://free-proxy-list.net/'
website_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,he;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

class Proxygetter():


    @staticmethod
    def check_if_ip(ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    @staticmethod
    def find_ips(soup):
        ips_list = []
        was_ip = False
        save_ip = ""
        for td in soup.findAll('td'):
            split_row = str(td).split("<td>")
            if len(split_row) > 1:
                split_row = split_row[1].split("</td>")[0]
                if (not was_ip) and (Proxygetter.check_if_ip(split_row)):
                    was_ip = True
                    save_ip = split_row
                elif was_ip:
                    if str(split_row) == '80':
                        ips_list.append(save_ip)
                    was_ip = False
        return ips_list

    @staticmethod
    def get_proxy():
        r = requests.get(website_site, website_headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        result = Proxygetter.find_ips(soup)
        if len(result) > 0:
            return result[0]


if __name__ == '__main__':
    print(Proxygetter.get_proxy())

