from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from urllib import request  # urllib.requestモジュールをインポート
from bs4 import BeautifulSoup, ResultSet  # BeautifulSoupクラスをインポート
import requests
import urllib.parse
import re
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import WebDriverException
import time


def spotify_playlist() -> None:
    SPOTIFY_ID: str = os.environ["SPOTIFY_ID"]
    SPOTIFY_SECRET: str = os.environ["SPOTIFY_SECRET"]
    client_id_secret = SpotifyClientCredentials(SPOTIFY_ID, SPOTIFY_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_id_secret)

    user = "nexus106106"
    playlist_id = "45KtjKqTE1UK55M16SfNrd"

    playlist_data = sp.user_playlist(user, playlist_id)
    # print(json.dumps(playlist_data, indent=2, ensure_ascii=False))

    # print(playlist_data["tracks"]["items"]["track"])

    tracks = playlist_data["tracks"]["items"]
    track_info = [
        (item["track"]["name"], [artist["name"] for artist in item["track"]["artists"]])
        for item in tracks
    ]
    print(track_info)


def beatport_search(driver: webdriver.chrome.webdriver.WebDriver) -> None:
    base_url = "https://www.beatport.com/search?q="
    search_words = "Multicoloured PSYQUI"
    escaped_query: str = urllib.parse.quote(search_words)
    final_url: str = f"{base_url}{escaped_query}"
    print(final_url)
    # response = requests.get(final_url, headers={'User-Agent': ''})

    driver.get(final_url)
    html = driver.page_source

    # print(response.text)

    soup = BeautifulSoup(html, "lxml")

    # script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

    # # 見つかった<script>タグの中身を出力します
    # if script_tag:
    #     print(script_tag.string)
    # else:
    #     print('指定したIDを持つ<script>タグが見つかりませんでした。')

    # data = json.loads(script_tag.string)
    # print(json.dumps(data, indent=2))

    desired_string: str = "TracksTable-style__ReleaseName"
    desired_string2: str = "ArtistNames-sc-"
    price_button: str = "AddToCart-style__"

    elements: ResultSet[Any] = soup.find_all(
        class_=re.compile(desired_string + "|" + desired_string2 + "|" + price_button)
    )
    # elements2 = soup.find_all(class_=re.compile(desired_string))

    for element in elements:
        print(element)


def beatport_playlist_create(driver: webdriver.chrome.webdriver.WebDriver, playlist_name: str, public: bool) -> None:
    url: str = "https://www.beatport.com/account/login?next=/library/playlists/new"
    try:
        driver.get(url)
    except WebDriverException as e:
        print(e)
        driver.quit()
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(
        os.environ["BEATPORT_USERNAME"]
    )
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(
        os.environ["BEATPORT_PASSWORD"]
    )
    driver.find_element(
        By.XPATH, '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/form/div/input'
    ).click()
    # name_box = driver.find_element(By.XPATH, '//*[@id="name"]')
    # name_box.send_keys("test")
    driver.find_element(By.XPATH, '//*[@id="name"]').send_keys(
        playlist_name
    )
    # プレイリスト名のボックス
    # Name must consist of only letters, numbers, underscore and dash
    if public is True:
        driver.find_element(
            By.XPATH, '//*[@id="new-playlist"]/div/div/div[2]/div[1]/div[2]/label/span/span'
        ).click()
    # プレイリストの公開非公開を切り替えるスイッチ、Trueの場合はクリック（非公開に設定）
    driver.find_element(
        By.XPATH, '//*[@id="new-playlist"]/div/div/div[2]/div[2]/div/button[2]'
    ).click()
    # saveボタンをクリック


    time.sleep(3)




load_dotenv()

# https://www.beatport.com/search?q=Multicoloured%20PSYQUI

driver: webdriver.chrome.webdriver.WebDriver = webdriver.Chrome()
driver.implicitly_wait(10)
# 待ち時間を設定

playlist_name: str = "test1"
beatport_playlist_create(driver, playlist_name, False)


driver.quit()
