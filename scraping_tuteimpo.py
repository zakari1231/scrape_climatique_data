import requests
from bs4 import BeautifulSoup
# import re
import pandas as pd
import os


def main():

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36/null'}

    url = 'https://en.tutiempo.net/climate/algeria.html'

    responce = requests.get(url, headers=headers)

    soup = BeautifulSoup(responce.text, 'html.parser')


    links = []
    for li in soup.find_all("li"):
        a_tag = li.find("a")
        if a_tag and a_tag.get("title") and a_tag["title"].startswith("Climate data:"):
            link = "https://en.tutiempo.net" + a_tag["href"]
            links.append(link)

    
    from_link_to_csv(links[12])


def retrive_title(link):
    url = link

    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    div = soup.find("div", class_="titulo")

    if div:
        h2 = div.find("h2")
        if h2:
            title_text = h2.text
            span = h2.find("span")
            if span:
                span_text = span.text
            else:
                span_text = None
        else:
            title_text = None
            span_text = None
    else:
        title_text = None
        span_text = None

    # title_text_new = title_text[7:]
    new_title = title_text.replace(" ", "_")
    new_title = new_title.replace(":", "")
    new_title = new_title.replace("-", "")
    return (new_title)
    # print(span_text) 

def retrive_all_years(link):
    url = link

    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    years_links = []
    for tr in soup.find_all("tr"):
        td = tr.find("td", class_="tc1")
        if td:
            a_tag = td.find("a")
            if a_tag:
                link = "https://en.tutiempo.net" + a_tag["href"]
                years_links.append(link)
    
    return years_links


# print (retrive_all_years(links[0]))

def retrive_all_month(year_link):
    response = requests.get(year_link)

    soup = BeautifulSoup(response.content, "html.parser")

    div = soup.find("div", class_="mlistados mt10")

    links_months = []
    if div:
        for li in div.find_all("li"):
            a_tag = li.find("a")
            if a_tag:
                link = "https://en.tutiempo.net" + a_tag["href"]
                links_months.append(link)

    return links_months 



def retrive_data_from_month(link):
    url = link

    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="medias mensuales numspan")

    if table:
        headers = [header.text for header in table.find_all("th")]
        headers = headers[:-1]
        rows = []
        for row in table.find_all("tr"):
            cells = [cell.text for cell in row.find_all("td")]
            if len(cells) == len(headers):
                rows.append(cells)

        data = {headers[i]: [row[i] for row in rows[:-1]] for i in range(len(headers))}
        df = pd.DataFrame(data)
        df.columns = headers
        return df
    else:
        print('table not fond')    




def retrive_years_data(links):
    dfs = []
    for link in links:
        df = retrive_data_from_month(link)
        dfs.append(df)
    final_df = pd.concat(dfs, ignore_index=True)
    return final_df


# adrar = retrive_all_years(links[0])
# print (adrar)

# first_month_adrar = retrive_all_month(adrar[1])

# print(retrive_years_data(first_month_adrar))


def from_link_to_csv(link):
    title = retrive_title(link)
    print(title)
    all_years = retrive_all_years(link)
    # print(all_years)
    all_months_links  = []
    for year in all_years:
        all_months = retrive_all_month(year)
        all_months_links.append(all_months)

    result_all_months_links = [item for sublist in all_months_links for item in sublist]

    # print(result_all_months_links)
    
    dfs = []
    for month_link in result_all_months_links:
        df = retrive_data_from_month(month_link)
        dfs.append(df)
    final_df = pd.concat(dfs, ignore_index=True)

    print(f'start {title}')
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(current_dir, f'{title}.csv')
    # final_df.to_csv(file_path, index=False)    
    final_df.to_csv(f'{title}.csv', index=False)
    print(f'finish {title}')




if __name__ =='__main__':
    main()