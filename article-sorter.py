import os
import csv
import shutil
import sys

def main():
    os.chdir("/absolute/path/to/desktop")
    
    article_numbers = []
    source_folder = input("Podaj nazwę folderu z plikami: ")
    source_csv = input("Podaj nazwę pliku csv (z końcówką .csv): ")
    articles_column = int(input("W której kolumnie znajdują się numery artykułów? "))
    is_header = input("Czy w csv jest rząd nagłówek (tak/nie)? ") == "tak"

    with open(source_csv, "rt") as file:
        filereader = csv.reader(file, delimiter=";")
        for row in filereader:
            article_numbers.append(row[int(articles_column)-1])
    
    article_numbers = article_numbers[1:] if is_header else article_numbers
    extract_folder = f'Extracted_files_{source_folder}'

    if not os.path.exists(extract_folder):
        os.mkdir(extract_folder)

    found = False
    for article_number in article_numbers:
        for filename in os.listdir(source_folder):
            if article_number in filename:
                shutil.copyfile(f'{source_folder}/{filename}', f'{extract_folder}/{filename}')
                found = True
                break
        if not found:
            print(f'Not found {article_number}')
        found = False

if __name__ == "__main__":
    main()
