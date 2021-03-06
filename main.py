import bs4, requests, sys

def html_find_all(page):
    soup = bs4.BeautifulSoup(page, "html.parser")
    return soup.findAll

def html_find(page):
    soup = bs4.BeautifulSoup(page, "html.parser")
    return soup.find

def get_hrefs(url):
    html = requests.get(url).content.decode()
    songs_devs = html_find_all(html)('div', {'class':'row', 'style':'font-size: 70%;'})
    for dev in songs_devs:
        name = dev.find_all('div')[0].text[1:].strip()
        url = 'https://ranatiphone.com/' + dev.find_all('a')[0]['href']
        yield (name, url)

def get_direct_url(url):
    r = requests.get(url)
    # data is decoded cuz it's hexa
    meta = html_find(r.content.decode())('meta')
    return meta['content'].split('URL=')[1]

def download(url, filename):
    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')
        if total is None:f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                file_size = round(total / (1024**2))
                file_down = round(downloaded / (1024**2))
                sys.stdout.write('\r[{}{}] [{}/{} MB]'.format('█' * done, ' ' * (50-done), file_down, file_size))
                sys.stdout.flush()

def main():
    print('''
██████╗  ██████╗ ███╗   ██╗██╗ █████╗     ███╗   ███╗██████╗ ██████╗     ██████╗ ██████╗  by: Khaled El-Morshedy
██╔══██╗██╔═══██╗████╗  ██║██║██╔══██╗    ████╗ ████║██╔══██╗╚════██╗   ██╔════╝██╔═══██╗
██║  ██║██║   ██║██╔██╗ ██║██║███████║    ██╔████╔██║██████╔╝ █████╔╝   ██║     ██║   ██║
██║  ██║██║   ██║██║╚██╗██║██║██╔══██║    ██║╚██╔╝██║██╔═══╝  ╚═══██╗   ██║     ██║   ██║
██████╔╝╚██████╔╝██║ ╚████║██║██║  ██║    ██║ ╚═╝ ██║██║     ██████╔╝██╗╚██████╗╚██████╔╝
╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝     ╚═════╝ ╚═╝ ╚═════╝ ╚═════╝''')
    album_url = input('\nEnter Album URL: ')
    
    # Get raw data (name, pop up url)
    print(f'\nExtracting Data from {album_url}')
    data = get_hrefs(album_url)
    for name, url in data:
        print(f'\nSearching for url in: {url}')
        
        # Extract direct url from pop up html
        direct_url = get_direct_url(url)
        
        # Download song with filtered name
        print(f'Downloading: {name}.mp3')
        download(direct_url, name + '.mp3')
        print()

if __name__ == '__main__':
    main()
