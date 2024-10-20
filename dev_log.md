# Development log

This file contains some notes I took while creating the application. They serve
the purpose of documenting the process and helping me to have remember some
aspects that might be of interest for future discussions on the decisions and
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
experience. Also it takes care of a lot of the payload validations automatically.

### Project structure

I'm using the usual Python package structure of having `src` be named as the
project name. In there I create multiple files to separate different the
definitions of routes, data model entities and their database representation.

## Implementing the solution

### Setting up the data model

After setting up a Hello World example and the main structure for the project,
I proceeded to work on getting the server connected to a database. I decided to
use an ORM for wase of use and developer ergonomics. This allows me to reuse a
lot of the logic for DB CRUD operations without having to write custom SQL
queries which are not required for now. I am using SQLAlchemy and used GenAI to
set up the code responsible for establishing a connection. Reason: the FastAPI
documentation has removed the code snippet to set this up as they now favor
`SQLModel`, an ORM package different than `SQLAlchemy`.

### Setting up the DB

I'm using PostgreSQL running on Docker. Reason: Data Model is clearly structured and
PostgreSQL scales very well within the expected load.

Docker compose came from GenAI.
