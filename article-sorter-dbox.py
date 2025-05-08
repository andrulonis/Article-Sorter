import os
import csv
import dropbox
import requests

def refresh_access_token(refresh_token, client_id, client_secret):
    token_url = "https://api.dropbox.com/oauth2/token"
    
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    
    response = requests.post(token_url, data=payload)
    tokens = response.json()
    return tokens.get("access_token")

def main():
    run_again = True
    
    dbx = dropbox.Dropbox(oauth2_access_token=refresh_access_token("<refresh_token>", "<client_id/app_key>", "<client_secret/app_secret>"), 
                          app_key="<client_id/app_key>",
                          app_secret="<client_secret/app_secret>")

    os.chdir("/absolute/path/to/desktop")

    while (run_again):
        article_numbers = []
        url = input("Podaj link do folderu docelowego na dropboxie: ")
        source_csv = input("Podaj nazwę pliku csv (z końcówką .csv): ")
        articles_column = int(input("W której kolumnie znajdują się numery artykułów? "))
        is_header = input("Czy w csv jest rząd nagłówek (tak/nie)? ") == "tak"

        shared_link = dropbox.files.SharedLink(url=url)

        with open(source_csv, "rt") as file:
            filereader = csv.reader(file, delimiter=";")
            for row in filereader:
                article_numbers.append(row[int(articles_column)-1])
        
        article_numbers = article_numbers[1:] if is_header else article_numbers
        total_articles = len(article_numbers)
        num_found = 0
        extract_folder = f'Extracted_files_{source_csv.split(".")[0]}'

        if not os.path.exists(extract_folder):
            os.mkdir(extract_folder)

        source_files = [] 
        has_more_files = True
        cursor = None
        while has_more_files:
            if cursor == None:
                result = dbx.files_list_folder(path="", shared_link=shared_link)
            else:
                result = dbx.files_list_folder_continue(cursor=cursor)
            source_files.extend(result.entries)
            cursor = result.cursor
            has_more_files = result.has_more

        found = False
        for article_number in article_numbers:
            for filename in [x.name for x in source_files]:
                if article_number in filename:
                    meta, resp = dbx.sharing_get_shared_link_file(url=url, path=f"/{filename}")
                    with open(f"{extract_folder}/{meta.name}.pdf", "wb") as f:
                        f.write(resp.content)
                    found = True
                    num_found += 1
                    break
            if not found:
                print(f'Not found {article_number}')
            found = False

        print(f'Extracted {num_found}/{total_articles}')
        run_again = input("Czy chcesz zacząć od nowa? ") == "tak"

if __name__ == "__main__":
    main()
