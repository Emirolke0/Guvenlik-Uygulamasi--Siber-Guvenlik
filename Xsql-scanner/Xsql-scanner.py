import requests
from bs4 import BeautifulSoup
import argparse
import warnings
from colorama import Fore, Style, init

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
init()

print(Fore.CYAN + "***************************************")
print(Fore.CYAN + "*                                     *")
print(Fore.CYAN + "*     Web Güvenlik Tarayıcısı         *")
print(Fore.CYAN + "*      XSS - SQL injection            *")
print(Fore.CYAN + "*             	                      *")
print(Fore.CYAN + "*       > Emir Batın Ölke <           *")
print(Fore.CYAN + "*       > Hakan Korkmaz   <           *")
print(Fore.CYAN + "*       > Oktay Halidi    <           *")
print(Fore.CYAN + "*                                     *")
print(Fore.CYAN + "*                                     *")
print(Fore.CYAN + "*     NAMIK KEMAL UNIVERSITESI        *")
print(Fore.CYAN + "*                                     *")
print(Fore.CYAN + "* Bu araç yalnızca eğitim amaçlıdır   *")
print(Fore.CYAN + "* ve yasa dışı kullanımı yasaktır.    *")
print(Fore.CYAN + "*                                     *")
print(Fore.CYAN + "***************************************" + Style.RESET_ALL)

def xss_scanner(url, xss_payload_file, verbose, output_file=None):
    print("\nXSS testi yapılıyor...")
    with open(xss_payload_file, 'r') as file:
        payloads = file.readlines()
    for payload in payloads:
        payload = payload.strip()
        if not payload:
            continue
        full_url = url + payload
        try:
            response = requests.get(full_url, verify=False)
        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"İstek hatası: {e}")
            continue
        if payload in response.text:
            print(Fore.RED + f"Payload {full_url} --> XSS Açığı Bulundu!" + Style.RESET_ALL)
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(f"Payload {full_url} --> XSS Açığı Bulundu!\n")
        elif verbose:
            print(Fore.GREEN + f"Payload {full_url} --> XSS Açığı Bulunamadı." + Style.RESET_ALL)
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(f"Payload {full_url} --> XSS Açığı Bulunamadı.\n")
    print(Fore.GREEN + "XSS Açığı Bulunamadı." + Style.RESET_ALL)
    print("---------------------------------------------")

def sql_injection_scanner(url, sql_payload_file, verbose, output_file=None):
    print("\nSQL Injection testi başlıyor...")
    with open(sql_payload_file, 'r') as file:
        payloads = file.readlines()
    error_messages = [
        "error in your SQL syntax",
        "Unclosed quotation mark after the character string",
        "[Microsoft][ODBC SQL Server Driver][SQL Server]Line 1: Incorrect syntax near",
        "ORA-01756: quoted string not properly terminated",
        "ERROR: syntax error at or near",
        "SQLCODE=-104, SQLSTATE=42601, SQLERRMC=;;SELECT * FROM USERS, DRIVER=4.8.87",
        "mysql_fetch_array() expects parameter 1 to be resource, boolean given"
    ]
    found = False
    for payload in payloads:
        payload = payload.strip()
        if not payload:  # Skip empty payloads
            continue
        full_url = url + payload
        try:
            response = requests.get(full_url, verify=False)
        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"İstek hatası: {e}")
            continue
        for error_message in error_messages:
            if error_message in response.text:
                print(Fore.RED + f"Payload {full_url} --> SQL Injection Açığı Bulundu!" + Style.RESET_ALL)
                if output_file:
                    with open(output_file, 'a') as f:
                        f.write(f"Payload {full_url} --> SQL Injection Açığı Bulundu!\n")
                found = True
        if verbose and not found:
            print(Fore.GREEN + f"Payload {full_url} --> SQL Injection Açığı Bulunamadı." + Style.RESET_ALL)
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(f"Payload {full_url} --> SQL Injection Açığı Bulunamadı.\n")
    if not found:
        print(Fore.GREEN + "SQL Injection Açığı Bulunamadı." + Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(description='Web Güvenlik Tarayıcısı')
    parser.add_argument('--url', type=str, help='Taranacak web sitesinin URL\'si')
    parser.add_argument('--xss-payload', type=str, help='XSS payloadlarının bulunduğu dosya yolu', default=None)
    parser.add_argument('--sql-payload', type=str, help='SQL Injection payloadlarının bulunduğu dosya yolu', default=None)
    parser.add_argument('-v', '--verbose', action='store_true', help='Detaylı çıktı')
    parser.add_argument('-o', '--output', type=str, help='Sonuçların yazılacağı dosya', default=None)
    args = parser.parse_args()
    url = args.url
    xss_payload_file = args.xss_payload
    sql_payload_file = args.sql_payload
    verbose = args.verbose
    output_file = args.output
    if xss_payload_file:
        xss_scanner(url, xss_payload_file, verbose, output_file)
    if sql_payload_file:
        sql_injection_scanner(url, sql_payload_file, verbose, output_file)

if __name__ == "__main__":
    main()
