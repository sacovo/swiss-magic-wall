# Swiss Election Map (SEMap)

Webapp to view voting results and projections for swiss referenda.

## Usage

Select a date and then a votation to view the map. Inside the map you can click on cantons and communes to get more detailed information. To go up a level you can click on the coat of arms on the top right.

You can toggle the cantons on and off to see all the communes at once, to do that you click on the coat of arms of Switzerland.

On the bottom right you have a card with more details about the selected canton or commune, click the titles to expand or hide.

There is also a table view, where you can sort and filter the cantons and communes, the link is on the bottom of the info-card.


## Setup

The `app` folder contains the angular app, that uses the json api served from the django backend.
You can configure the url under wich the frontend accesses the databse in the app/src/environments files for your environment.

The django app has a Dockefile that just serves the api, the angular app has a Dockerfile for an nginx container with the compiled files in the root and proxy for the django urls.

See docker-compose.example.yml for inspiration on how to setup the whole thing.

## Development

Definition in docker-compose.yml runs the django backend on port 8000 and the angular frontend on port 4200.
Urls `/api, /admin and /static` are proxied to the django backend, so you can acces those over `localhost:4200/api` ...

Bring all services up:
```
docker-compose up
```

Setup the database:

```
docker-compose exec web python manage.py migrate
```

Create a superuser
```
docker-compose exec web python manage.py createuser
```

Login under http://localhost:4200/admin or http://localhost:8000/admin/ and add a voting day with a json url from [here](https://opendata.swiss/de/dataset/echtzeitdaten-am-abstimmungstag-zu-eidgenoessischen-abstimmungsvorlagen).

Select the created voting day in the admin interface and execute the action to initiate the voting day. This will fetch the results and populate the database with the communes and cantons.

After that you can inspect the voting day under http://localhost:4200/
