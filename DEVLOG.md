# Development log

This file contains some notes I took while creating the application. They serve
the purpose of documenting the process and helping me remember some
aspects that might be of interest for future discussions about the decisions and
approaches I used.

## Setting up the project

### Programming language

I'm using Python since it's my main programming language at the moment and
allows me to get things up and running quite fast with minimal number of lines
of code.

### Development environment

I set up the project by hand using `uv`, a faster and more useful version of
`pip` with `poetry` like functionality. You can think of it as Python's version
of Rust's `cargo`.

### Dependencies

I went with FastAPI because of my current experience with it, it's ease of use
and because it allows me to iterate quickly with a really smooth developer
experience. It takes care of a bunch of payload validations automatically
and also comes with a Swagger/OpenAPI docs page for free.

### Project structure

I'm using the usual Python package structure of having `src` be named as the
project name. In there, I create multiple files to separate the different
definitions of routes, data model entities and their database representation.

## Implementing the solution

After setting up a Hello World example and the main structure for the project,
I proceeded to work on getting the server connected to a database.

### Setting up the DB

I'm using PostgreSQL running on Docker. Reason: Data Model is clearly
structured and PostgreSQL scales very well within the expected load.

Eventually, the database will probably become the bottleneck but we can deal
with that later. Possible solutions would be vertical scaling, sharding or
eventually moving to a distributed DB like CockroachDB, Cassandra or DynamoDB.
This is not something we should plan for at this stage.

Docker compose came from GenAI. I just extracted the credentials to a
`.env-example` file.

### Setting up the data model

I decided to use an ORM for ease of use and developer ergonomics. This allows
me to reuse a lot of the logic for DB CRUD operations without having to write
custom SQL queries which are not required for now. I am using SQLAlchemy and
used GenAI to set up the code responsible for establishing a connection.
Reason: the FastAPI documentation has replaced `SQLAlchemy` in favor of
`SQLModel`, a wrapper of SQLAlchemy written by the FastAPI author.

#### Adding stations

Data model

- Added a customer entity to separate data between different customers.
Column is nullable for now for easier testing. Auth & RBAC are out of scope for
now.
- Kept all column types as Strings(=varchar 255) for simplicity.
- For better UX, we should add an endpoint to produce address suggestions based
on user input via a third-party API. This gives us the exact coordinates of the
location which would allow map visualizations. For now, coordinates are optional.

Endpoints

- No auth for now. Users can access all the data.

#### Adding transformers, connections and devices

Data model

- Added an `external_id` field to allow for better integrations with existing systems.
- Kept transformers and connections slim, skipped distributors as another
entity won't make difference for the first iteration.
- Added device types and component types to devices. Allows to record all
devices in the same table. This is simple enough to begin with and makes it
easier to extend to new devices or devices been moved across components.
- Configs and specs are JSON objects. Configs should probably be reusable across
devices. Figuring out if this is a requirement is out of scope for now.
Can be easily changed in the future.

Endpoints

- A PATCH request to specific fields in a device config/spec will not work as
expected :/ They will replace the whole config/spec, instead of updating the
specified fields only. Left a comment in the code, should be fixed before prod :)

#### Adding measurements

Data model

- Added all the components hierarchy explicitly to each measurement.
When persisting a measurement received from device X, we look up the component
that the device is attached to, and the corresponding
connection/transformer/station ID. We store all those IDs in the table
directly. This makes READs more performant, avoiding joins when querying data
for specific components, for the price of being a bit more work on WRITEs.
- Added `measured_at` and `sent_at` timestamps to measure the latency of the system.
My assumption is that devices of type `SENSOR` gather measurements and
communicate those to devices of type `EDGE`. There they are grouped into
batches that are sent to the application via an HTTP POST. Once we start
processing the measurements asynchronously in our application (to reduce the
stress on the system when spikes in the measurements endpoint are detected), we
might also introduce latency between the time a measurement is received until a
measurement is persisted (and available to API clients). These two new fields,
together with the `created_at` timestamp, will allow to measure that latency
and assign it to the correct step of the process.

Endpoints

- A POST endpoint for creating measurements in batches and as individual entities.
- A GET endpoint to read measurements from a specific station. Implements
pagination, allows passing query params for transformer/connection ID, and
start and end date to query for a specific time range.
