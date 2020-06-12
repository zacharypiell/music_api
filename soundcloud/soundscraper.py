from selenium import webdriver
import requests
import bs4
import os
import time

# when in the song url
def show_related_tracks(browser):
    related_button = browser.find_elements_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[3]/div[2]/div[1]/article[2]/a/h3")[0]
    related_button.click()



    request = browser.find_elements_by_xpath("/html")
    soup = bs4.BeautifulSoup(request.text, "lxml")





top_url = "http://soundcloud.com/charts/top"
new_url = "http://soundcloud.com/charts/new"
track_url = "http://souncloud.com/search/sounds?q="
artist_url = "http://souncloud.com/search/people?q="
mix_url_end = "&filter.duration=long"

print("this is running...")
# create selenium browser
browser = webdriver.Chrome("/Users/zackpiell/chromedriver")
browser.get("https://soundcloud.com")

# main menu
print()
print(">>> Welcome to Python SoundCloud Scraper")
print(">>> Explore the Top / New Charts for all Genres")
print(">>> Search for tracks, artists, and mixes")

while True:
    print(">>> Menu")
    print(">>> 1 - Search for Track")
    print(">>> 2 - Search for Artist")
    print(">>> 3 - Search for Mix")
    print(">>> 4 - Top Charts")
    print(">>> 5 - New & Hot Charts")
    print(">>> 0 - Exit")
    print()

    choice = int(input(">>> Your Choice: "))

    if (choice == 0):
        browser.quit()
        break
    print()

    if (choice == 1):
        name = input("Name of track: ")
        print()
        "%20".join(name.split(" ")) # replace spaces
        browser.get(track_url + name)
        play_it = input("Play Top Result? (y/n) ")
        if play_it == 'y':
            song_click = browser.find_elements_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div/div/div/ul/li[1]/div/div/div/div[2]/div[1]/div/div/div[2]/a")[0]
            song_click.click()
            play_button = browser.find_elements_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/a")[0]
            time.sleep(0.5)
            play_button.click()

            related_tracks = input("See Related Tracks? (y/n)")
            if related_tracks == 'y':
                show_related_tracks(browser)
            else: continue



        print()
        continue
    if (choice == 2):
        name = input("Artist Name: ")
        print()
        "%20".join(name.split(" ")) # replace spaces
        browser.get(artist_url + name)
        print()
        continue
    if (choice == 3):
        name = input("Name of mix: ")
        print()
        "%20".join(name.split(" ")) # replace spaces
        browser.get(track_url + name + mix_url_end)
        play_it = input("Play Top Result? (y/n) ")
        if play_it == 'y':
            play_button = browser.find_elements_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div/div/div/ul/li[1]/div/div/div/div[2]/div[1]/div/div/div[1]")[0]
            time.sleep(0.5)
            play_button.click()
        print()
        continue
    if (choice == 4):
        request = requests.get(top_url)
        soup = bs4.BeautifulSoup(request.text, "lxml")
        # print(request.text)
        while True:
            print("Genres Available:")
            genres = soup.select("a[href*=genre]")[2:]
            genre_links = []
            for index, genre in enumerate(genres):
                print(str(index) + ": " + genre.text)
                genre_links.append(genre.get("href"))
            print()
            choice = input(">>> Your choice (x to go back to the main menu): ")
            if choice == 'x':
                break
            else:
                choice = int(choice)
            url = "http://soundcloud.com" + genre_links[choice]
            request = requests.get(url)
            soup = bs4.BeautifulSoup(request.text, "lxml")

            tracks = soup.select("h2")[3:]
            track_links = []
            track_names = []

            for index, track in enumerate(tracks):
                track_links.append(track.a.get("href"))
                track_text = track.text.replace("\n"," ")
                track_names.append(track_text)
                print(str(index + 1) + ": " + track_text)

            while True:
                choice = input(">>> Your choice (x to re-select new genre): ")
                print()
                if choice == 'x':
                    break
                else:
                    choice = int(choice) - 1
                print("Now Playing: " + track_names[choice])
                browser.get("http://souncloud.com" + track_links[choice])

                play_button = browser.find_elements_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/a")[0]
                time.sleep(0.5)
                play_button.click()


    if choice == 5: #get new and hot tracks for genre
        request = requests.get(new_url)
        soup = bs4.BeautifulSoup(request.text, "lxml")
        # print(request.text)
        while True:
            print("Genres Available:")
            genres = soup.select("a[href*=genre]")[2:]
            genre_links = []
            for index, genre in enumerate(genres):
                print(str(index) + ": " + genre.text)
                genre_links.append(genre.get("href"))
            print()
            choice = input(">>> Your choice (x to go back to the main menu): ")
            if choice == 'x':
                break
            else:
                choice = int(choice)
            url = "http://soundcloud.com" + genre_links[choice]
            request = requests.get(url)
            soup = bs4.BeautifulSoup(request.text, "lxml")

            tracks = soup.select("h2")[3:]
            track_links = []
            track_names = []

            for index, track in enumerate(tracks):
                track_links.append(track.a.get("href"))
                track_text = track.text.replace("\n"," ")
                track_names.append(track_text)
                print(str(index + 1) + ": " + track_text)
            while True:
                choice = input(">>> Your choice (x to re-select new genre): ")
                print()
                if choice == 'x':
                    break
                else:
                    choice = int(choice) - 1
                print("Now Playing: " + track_names[choice])
                browser.get("http://souncloud.com" + track_links[choice])

                play_button = browser.find_elements_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/a")[0]
                time.sleep(0.5)
                play_button.click()


    # add a related tracks code snippet when playing a song

    # add similar artists snippet (maybe demo each artist?)

    # start station

    print("Seeya Later")
    print()
