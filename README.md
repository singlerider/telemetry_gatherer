# Cockpit

A simple telemetry-fetcher scaffold.

## Build and Run

This repository has been built to be easy to run. Immediately on running the [./runserver.sh](/runserver.sh) script, the project will run migrations and load mock data from a fixture located in [/cockpit/telemetry/fixtures/telemetry_app_data.json](/cockpit/telemetry/fixtures/telemetry_app_data.json).

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

The UUIDs included in the below example are provided from the fixtures (mock data) mentioned above.

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

## Testing

```shell
$ pytest
```
