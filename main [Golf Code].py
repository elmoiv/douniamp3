import bs4, requests, sys

get_direct_url = lambda url: bs4.BeautifulSoup(page, "html.parser").find(requests.get(url).content.decode())('meta')['content'].split('URL=')[1]
get_hrefs = lambda url: [(dev.find_all('div')[0].text[1:].strip(), 'https://ranatiphone.com/' + dev.find_all('a')[0]['href']) for dev in bs4.BeautifulSoup(page, "html.parser").findAll(requests.get(url).content.decode())('div', {'class':'row', 'style':'font-size: 70%;'})]
def download(url, filename):
    with open(filename, 'wb') as f:
        rsp = requests.get(url, stream=True); total = rsp.headers.get('content-length')
        if total is None:f.write(response.content)
        else:
            downloadedm total = 0, int(total)
            for data in rsp.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data); f.write(data)
                done, file_size, file_down = int(50*downloaded/total), round(total / (1024**2)), round(downloaded / (1024**2))
                sys.stdout.write('\r[{}{}] [{}/{} MB]'.format('█' * done, ' ' * (50-done), file_down, file_size)); sys.stdout.flush()
def main():
    print('''██████╗  ██████╗ ███╗   ██╗██╗ █████╗     ███╗   ███╗██████╗ ██████╗     ██████╗ ██████╗  by: Khaled El-Morshedy
██╔══██╗██╔═══██╗████╗  ██║██║██╔══██╗    ████╗ ████║██╔══██╗╚════██╗   ██╔════╝██╔═══██╗
██║  ██║██║   ██║██╔██╗ ██║██║███████║    ██╔████╔██║██████╔╝ █████╔╝   ██║     ██║   ██║
██║  ██║██║   ██║██║╚██╗██║██║██╔══██║    ██║╚██╔╝██║██╔═══╝  ╚═══██╗   ██║     ██║   ██║
██████╔╝╚██████╔╝██║ ╚████║██║██║  ██║    ██║ ╚═╝ ██║██║     ██████╔╝██╗╚██████╗╚██████╔╝
╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝     ╚═════╝ ╚═╝ ╚═════╝ ╚═════╝''')
    album_url = input('\nEnter Album URL: '); print(f'\nExtracting Data from {album_url}'); data = get_hrefs(album_url)
    for name, url in data: print(f'\nSearching for url in: {url}'); direct_url = get_direct_url(url); print(f'Downloading: {name}.mp3'); download(direct_url, name + '.mp3'); print()
if __name__ == '__main__':
    main()
