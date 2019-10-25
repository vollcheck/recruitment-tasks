#!/usr/bin/python
import csv


def download():
    with open("movies.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)


if __name__ == "__main__":
    download()
