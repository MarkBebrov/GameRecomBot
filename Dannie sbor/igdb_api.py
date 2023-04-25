import requests
import json

def get_twitch_token(client_id, client_secret):
    url = "https://id.twitch.tv/oauth2/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=payload)
    return json.loads(response.text)["access_token"]

def igdb_request(access_token, query):
    url = "https://api.igdb.com/v4/games"
    headers = {
        "Client-ID": "wab80agadimektk5r7ck4qi74kg1m9",
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    response = requests.post(url, headers=headers, data=query)
    return json.loads(response.text)

def fetch_games(access_token, limit=500, offset=0):
    query = f"""
    fields name, genres.name, platforms.name, release_dates.date, rating, summary;
    limit {limit};
    offset {offset};
    """
    return igdb_request(access_token, query)


def main():
    client_id = "секрет"
    client_secret = "секрет"

    access_token = get_twitch_token(client_id, client_secret)
    games_data = []

    offset = 0
    while True:
        print(f"Fetching games with offset {offset}...")
        games_batch = fetch_games(access_token, limit=500, offset=offset)
        if not games_batch:
            break
        games_data.extend(games_batch)
        offset += 500

    with open("games_data.json", "w", encoding="utf-8") as file:
        json.dump(games_data, file, ensure_ascii=False, indent=4)

    print(f"Total games fetched: {len(games_data)}")

if __name__ == "__main__":
    main()
