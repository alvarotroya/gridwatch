# Presentation Notes

This file contains the rough structure to follow while presenting the solution.

## Short presentation

- Who am I?
- What do I do now?
- What do I want to do next?

## Overview of the problem

### Requirements

Design CRUD API to model:

- Energy grid components:
  - Stations, Transformers, Low-voltage-distributors, Connections (=Abgänge).
- Measurement devices of different types and configurations.
- Receive and store measurements from measurement devices.
- Retreive measurement data of a given station for a given period of time.
- Design should be easy to extend to more devices or components.

### Objectives

We want to use the prototype to discuss:

- Data model design
- API design
- Implementation approach
- Scalability, reliability, durability, performance and trade-offs

## Demo

A lot of the decisions taken while writing the code are documented in [DEVLOG.md](/DEVLOG.md).

1. Demo data model using DB.
1. Demo API using openAPI.
1. Discuss tech stack.
1. Explore code on Github.
1. Discuss possible improvements of the architecture.
1. Discuss how to make the prototype production-ready.
