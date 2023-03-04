# README

## clients

| Column     | Type | Description                                             |
|------------|------|---------------------------------------------------------|
| `index`    | int  | A unique identifier for each client                     |
| `firstname`| str  | The first name of the client                            |
| `surname`  | str  | The surname of the client                                |
| `reference`| str  | A unique reference number for the client                 |
| `firm`     | str  | The company that the client works for                    |
| `role`     | str  | The client's role within the company                     |
| `cin`      | str  | The client's national identification number              |
| `email`    | str  | The client's email address                               |

This database contains information about clients of a company.

## events

| Column     | Type | Description                                             |
|------------|------|---------------------------------------------------------|
| `index`    | int  | A unique identifier for each event                      |
| `time`     | str("%H:%M:%S")  | The start time of the event                              |
| `type`     | str(CONF,ATLR,TUTO)  | The type of event (e.g. meeting, conference, presentation)|
| `lecturer` | str  | The name of the person who will deliver the event        |
| `day`      | str(range(1,6))  | The date on which the event will take place              |

This database contains information about events organized by a company.

## clients_events

| Column         | Type  | Description                                                       |
|----------------|-------|-------------------------------------------------------------------|
| `index`        | int   | A unique identifier for each row                                   |
| `id_client`    | int   | The index of the client attending the event                        |
| `id_event`     | int   | The index of the event that the client is attending                 |
| `is_present`   | bool  | A flag indicating whether the client attended the event or not    |
| `time_presence`| str("%H:%M:%S") or null   | The time at which the client arrived at the event                   |

This database contains information about clients attending events.
