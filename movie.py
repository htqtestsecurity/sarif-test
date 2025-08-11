import json

import requests


def get_director_movies(person_id):
    url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?language=ko-KR"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZWM2MzJiYzRkMTE1ODE0ODEyZmIxZWQyZGI4MmIyYSIsInN1YiI6IjYzZDMxNzdjNWEwN2Y1MDBhMjk3NzcwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XMg3HVBIalS4AapKFG0HlLXlGD2ovdUMZR6nTZG-55o"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    crew_data = data['crew']

    tmp_lst = []
    # job == director 인거 중에서만
    for i in range(len(crew_data)):
        if crew_data[i]['job'] == 'Director':
            tmp_lst.append((crew_data[i]['vote_average'], crew_data[i]['id']))

    tmp_lst.sort(key=lambda x: x[0], reverse=True)

    tmp_set = set()
    for i in range(len(tmp_lst)):
        # 같은 감독의 영화 개수
        if len(tmp_set) >= 6:
            return tmp_set

        tmp_set.add(tmp_lst[i][1])

    else:
        return tmp_set
def get_video(movie_id, title):
    url1 = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=ko-KR"
    url2 = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZWM2MzJiYzRkMTE1ODE0ODEyZmIxZWQyZGI4MmIyYSIsInN1YiI6IjYzZDMxNzdjNWEwN2Y1MDBhMjk3NzcwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XMg3HVBIalS4AapKFG0HlLXlGD2ovdUMZR6nTZG-55o"
    }

    response1 = requests.get(url1, headers=headers)
    response2 = requests.get(url2, headers=headers)

    data1 = response1.json()
    data2 = response2.json()
    for i in data1['results']:
        if title in i['name'] and i['official']:
            return i['key']
        elif title in i['name']:
            return i['key']

    for i in data2['results']:
        if 'Official Trailer' in i['name']:
            return i['key']
        elif 'Trailer' in i['name']:
            return i['key']
def get_credit(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=ko-KR"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZWM2MzJiYzRkMTE1ODE0ODEyZmIxZWQyZGI4MmIyYSIsInN1YiI6IjYzZDMxNzdjNWEwN2Y1MDBhMjk3NzcwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XMg3HVBIalS4AapKFG0HlLXlGD2ovdUMZR6nTZG-55o"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    for i in data['crew']:
        if i['job'] == "Director":
            person_id = i['id']
            return i['name'], person_id
def get_popular():
    base_url = 'https://api.themoviedb.org/3'
    path = '/movie/popular'

    params = {
        'api_key': '1ec632bc4d115814812fb1ed2db82b2a',
        'language': 'ko',
        'page': 0
    }
    lst = []
    movie_name = []
    person_lst = []
    # 원하는 페이지 수만큼 받기
    for i in range(1, 20):
        params['page'] = i
        res_genre = requests.get(base_url + path, params=params)
        genre_list = res_genre.json()

        for j in range(len(genre_list['results'])):
            if genre_list['results'][j]['vote_count'] >= 100:
                movie_id = genre_list['results'][j]['id']
                try:
                    director, person_id = get_credit(movie_id)
                except TypeError:
                    continue
                preview = get_video(
                    movie_id, genre_list['results'][j]['title'])

                if (director, person_id) not in person_lst:
                    person_lst.append((director, person_id))

                try:
                    lst.append({"model": "movies.movie",
                                "fields": {'title': genre_list['results'][j]['title'],
                                           'movie_id': genre_list['results'][j]['id'],
                                           'overview': genre_list['results'][j]['overview'],
                                           'poster_path': genre_list['results'][j]['poster_path'],
                                           'release_date': genre_list['results'][j]['release_date'],
                                           'director': director,
                                           'trailer_key': preview,
                                           'vote_average': genre_list['results'][j]['vote_average']}})
                    movie_name.append(genre_list['results'][j]['title'])
                except KeyError:
                    continue

    print(len(person_lst))

    for i in range(len(person_lst)):
        director = person_lst[i][0]
        llst = get_director_movies(person_lst[i][1])

        for j in llst:
            url = f"https://api.themoviedb.org/3/movie/{j}?language=ko-KR"

            headers = {
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZWM2MzJiYzRkMTE1ODE0ODEyZmIxZWQyZGI4MmIyYSIsInN1YiI6IjYzZDMxNzdjNWEwN2Y1MDBhMjk3NzcwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XMg3HVBIalS4AapKFG0HlLXlGD2ovdUMZR6nTZG-55o"
            }

            response = requests.get(url, headers=headers)
            add_genre = response.json()

            preview = get_video(
                add_genre['id'], add_genre['title'])

            try:
                if add_genre['title'] not in movie_name and add_genre['vote_count'] >= 50:
                    lst.append({"model": "movies.movie",
                                "fields": {'title': add_genre['title'],
                                           'movie_id': add_genre['id'],
                                           'overview': add_genre['overview'],
                                           'poster_path': add_genre['poster_path'],
                                           'release_date': add_genre['release_date'],
                                           'director': director,
                                           'trailer_key': preview,
                                           'vote_average': add_genre['vote_average']}})
            except KeyError:
                continue

    return lst


# title, id,overview, poster_path, release_date, director, trailer_key
movie_lst = get_popular()

# 영화 총 개수
print(len(movie_lst))

with open('movie.json', 'w', encoding='utf-8') as f:
    json.dump(movie_lst, f, ensure_ascii=False, indent=2)
