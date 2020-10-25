# Cockpit

A simple telemetry-fetcher scaffold.

## Limitations

The main limitation/bug is multiple (`n`) concurrent subscriptions will result in `n` responses to each respective client. This is likely due to initial handshake logic in how the websockets are establishing connections.

This repository is meant as a template, not as a completed application. The exposed `SECRET_KEY` is left unchanged intentionally for reproducible password hashes for a mock data fixture (described below).

## Build and Run

This repository has been built to be easy to get going quickly. Immediately on executing the [./runserver.sh](/runserver.sh) script, the project will run migrations and load mock data from a fixture located in [/cockpit/telemetry/fixtures/telemetry_app_data.json](/cockpit/telemetry/fixtures/telemetry_app_data.json).

### Virtual Environment

```shell
$ pip install -requirements.txt
$ ./runserver.sh
```

### Docker


```shell
$ ./build.sh
$ ./rundocker.sh
```

## Explore

### GraphIQL

Open your browser to [0.0.0.0:8000/graphql](http://0.0.0.0:8000/graphql).


#### Check Most Recent Temperature (Telemetry) Entry

```graphql
query {
  currentTemperature {
    timestamp
    value
    unit
  }
}
```

#### Subscribe to New Temperature (Telemetry) Entries

```graphql
subscription {
  currentTemperatureSubscribe {
    temperature {
      timestamp
      value
      unit
    }
  }
}
```

#### Create a New Telemetry Entry

The UUIDs included in the below example are provided from the fixtures (mock data) mentioned above. Executing this while subscribing to the above will trigger that subscription with an appropriate response.

```graphql
mutation createTelemetryEntry {
  createTelemetryEntry(
    sensorId: "4d862cef-df65-4f7e-9bdd-711fe068ccaa"
    machineId:"a93a5bc8-b962-4373-8a41-01e29d02811a"
    value: "5.0"
    createdById:"8d8ceaf8-91dd-4c73-b08e-8d2843ccb6fc"
  ) {
    telemetryEntry {
      id
      value
      sensor {
        id
        name
        category
        unit
      }
      machine {
        id
        name
        sensors {
          id
        }
      }
    }
  }
}
```

### Admin

The admin interface is also available at [0.0.0.0:8000/admin](0.0.0.0:8000/admin).

Username: `singlerider`

Password: `python3.9`

## Testing

```shell
$ ./runtests.sh
```
