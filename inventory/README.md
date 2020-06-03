# Inventory Service
Service contains main database with information about films

## Database
Database of the service is MongoDB replica set with 3 nodes.

Film documents structure:
```
{
id: <:int>,
title_alphanum: <:string>,
primary_title: <:string>,
is_adult: <:boolean>,
start_year: <:int>,
runtime_minutes: <:int>,
genres: <:list:string>,
directors: <:list:string>,
average_rating: <:float>,
num_votes: <:int>,
price: <:float>
}
```

## API
All requests and responses manipulate with JSON format.
All responses contain _success_ and _error_ fields.

- get_by_id(_request_) <br />
method: `GET` <br />
address: `/service_app/id/` <br />
request format:
`{film_id: <:int>}` <br />
response format:
`{success: <:boolean>, error: <:string>, film: <:dict>}`

- enum_ids(_request_) <br />
method: `GET` <br />
address: `/service_app/enum/` <br />
request format:
`{}` <br />
response format:
`{success: <:boolean>, error: <:string>, ids: <:list:int>}`

- get_by_title(_request_) <br />
method: `POST` <br />
address: `/service_app/title/` <br />
request format:
`{primary_title: <:string>}` <br />
response format:
`{success: <:boolean>, error: <:string>, films: <:list:dict>}`

- get_filtered_films(_request_) <br />
method: `POST` <br />
address: `/service_app/filter/` <br />
request format:
```
{filters: {is_adult: <:boolean>,
            start_year: <:int>,
            runtime_minutes: <:int>,
            genres: <:string>,
            average_rating: <:float>}}
```
response format:
`{success: <:boolean>, error: <:string>, films: <:list:dict>}`

- vote_for_film(_request_) <br />
method: `POST` <br />
address: `/service_app/vote/` <br />
request format:
`{film_id: <:int>, mark: <:float>}` <br />
response format:
`{success: <:boolean>, error: <:string>}`
