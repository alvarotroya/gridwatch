-- A simple SQL script to populate the database, this should be solved by a migration tool like Alembic but this was easy enough for now


-- Type definitions

CREATE TYPE public."devicetype" AS ENUM (
	'EDGE',
	'SENSOR_1');

CREATE TYPE public."componenttype" AS ENUM (
	'TRANSFORMER',
	'CONNECTION');

CREATE TYPE public."healthstatus" AS ENUM (
	'OK',
	'DETERIORATED',
	'UNREACHABLE');

CREATE TYPE public."measurementtype" AS ENUM (
	'VOLTAGE',
	'CURRENT');

-- Table definitions

CREATE TABLE IF NOT EXISTS customers (
        id UUID NOT NULL,
        name VARCHAR,
        PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS devices (
        id UUID NOT NULL,
        name VARCHAR,
        device_type devicetype,
        component_id UUID,
        component_type componenttype,
        device_specs JSONB,
        device_config JSONB,
        health_status healthstatus,
        last_healthcheck_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        installed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        external_id VARCHAR,
        customer_id UUID,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        PRIMARY KEY (id),
        FOREIGN KEY(customer_id) REFERENCES customers (id)
);

CREATE TABLE IF NOT EXISTS stations (
        id UUID NOT NULL,
        external_id VARCHAR,
        name VARCHAR,
        customer_id UUID,
        street VARCHAR,
        house_number VARCHAR,
        city VARCHAR,
        state VARCHAR,
        zip_code VARCHAR,
        country VARCHAR,
        latitude FLOAT,
        longitude FLOAT,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        PRIMARY KEY (id),
        FOREIGN KEY(customer_id) REFERENCES customers (id)
);

CREATE TABLE IF NOT EXISTS transformers (
        id UUID NOT NULL,
        name VARCHAR,
        customer_id UUID,
        station_id UUID NOT NULL,
        external_id VARCHAR,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        PRIMARY KEY (id),
        FOREIGN KEY(customer_id) REFERENCES customers (id),
        FOREIGN KEY(station_id) REFERENCES stations (id)
);

CREATE TABLE IF NOT EXISTS connections (
        id UUID NOT NULL,
        name VARCHAR,
        customer_id UUID,
        transformer_id UUID NOT NULL,
        external_id VARCHAR,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        PRIMARY KEY (id),
        FOREIGN KEY(customer_id) REFERENCES customers (id),
        FOREIGN KEY(transformer_id) REFERENCES transformers (id)
);

CREATE TABLE IF NOT EXISTS measurements (
        id UUID NOT NULL,
        station_id UUID,
        transformer_id UUID,
        connection_id UUID,
        device_id UUID,
        value FLOAT,
        measurement_type measurementtype,
        measured_at TIMESTAMP WITHOUT TIME ZONE,
        sent_at TIMESTAMP WITHOUT TIME ZONE,
        customer_id UUID,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        PRIMARY KEY (id),
        FOREIGN KEY(station_id) REFERENCES stations (id),
        FOREIGN KEY(transformer_id) REFERENCES transformers (id),
        FOREIGN KEY(connection_id) REFERENCES connections (id),
        FOREIGN KEY(device_id) REFERENCES devices (id),
        FOREIGN KEY(customer_id) REFERENCES customers (id)
);


-- Stations

INSERT INTO public.stations
(id, "name", customer_id, street, house_number, city, state, zip_code, country, latitude, longitude, created_at, updated_at, external_id)
VALUES('10000000-0000-0000-0000-000000000000'::uuid, 'Station 1', NULL, 'Zeppelinstraße', '7d', 'Karlsruhe', 'Baden-Württemberg', '76185', 'Germany', 49.002403, 8.364468, '2024-10-22 08:07:44.752', '2024-10-22 08:07:44.752', 'station_1_external_id')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.stations
(id, "name", customer_id, street, house_number, city, state, zip_code, country, latitude, longitude, created_at, updated_at, external_id)
VALUES('20000000-0000-0000-0000-000000000000'::uuid, 'Station 2', NULL, 'Grünwinkel', '15', 'Karlsruhe', 'Baden-Württemberg', '76185', 'Germany', 49.002403, 8.364468, '2024-10-22 09:07:44.752', '2024-10-22 08:07:44.752', 'station_2_external_id')
ON CONFLICT (id) DO NOTHING;

-- Transformers

INSERT INTO public.transformers
(id, "name", customer_id, station_id, external_id, created_at, updated_at)
VALUES('00000000-1000-0000-0000-000000000000'::uuid, 'Transformer 1', NULL, '10000000-0000-0000-0000-000000000000'::uuid, 'transformer_1_external_id', '2024-10-22 08:28:57.015', '2024-10-22 08:28:57.015')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.transformers
(id, "name", customer_id, station_id, external_id, created_at, updated_at)
VALUES('00000000-2000-0000-0000-000000000000'::uuid, 'Transformer 2', NULL, '10000000-0000-0000-0000-000000000000'::uuid, 'transformer_2_external_id', '2024-10-22 08:28:57.015', '2024-10-22 09:28:57.015')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.transformers
(id, "name", customer_id, station_id, external_id, created_at, updated_at)
VALUES('00000000-3000-0000-0000-000000000000'::uuid, 'Transformer 3', NULL, '20000000-0000-0000-0000-000000000000'::uuid, 'transformer_3_external_id', '2024-10-22 08:28:57.015', '2024-10-22 10:28:57.015')
ON CONFLICT (id) DO NOTHING;

-- Connections

INSERT INTO public.connections
(id, "name", customer_id, transformer_id, external_id, created_at, updated_at)
VALUES('00000000-0000-1000-0000-000000000000'::uuid, 'Connection 1', NULL, '00000000-1000-0000-0000-000000000000'::uuid, 'connection_1_external_id', '2024-10-23 17:38:07.546', '2024-10-23 17:38:07.546')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.connections
(id, "name", customer_id, transformer_id, external_id, created_at, updated_at)
VALUES('00000000-0000-2000-0000-000000000000'::uuid, 'Connection 2', NULL, '00000000-1000-0000-0000-000000000000'::uuid, 'connection_2_external_id', '2024-10-23 18:38:07.546', '2024-10-23 18:38:07.546')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.connections
(id, "name", customer_id, transformer_id, external_id, created_at, updated_at)
VALUES('00000000-0000-3000-0000-000000000000'::uuid, 'Connection 3', NULL, '00000000-2000-0000-0000-000000000000'::uuid, 'connection_3_external_id', '2024-10-23 18:38:07.546', '2024-10-23 18:38:07.546')
ON CONFLICT (id) DO NOTHING;

-- Devices

INSERT INTO public.devices
(id, "name", device_type, component_id, component_type, device_specs, device_config, health_status, last_healthcheck_at, installed_at, external_id, customer_id, created_at, updated_at)
VALUES('00000000-0000-0000-1000-000000000000'::uuid, 'Sensor 1', 'SENSOR_1'::public."devicetype", '00000000-0000-1000-0000-000000000000'::uuid, 'CONNECTION'::public."componenttype", '{}'::jsonb, '{}'::jsonb, 'OK'::public."healthstatus", '2024-10-23 17:41:53.635', '2024-10-23 17:41:53.635', 'sensor_1_external_id', NULL, '2024-10-23 17:41:53.635', '2024-10-23 17:41:53.635')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.devices
(id, "name", device_type, component_id, component_type, device_specs, device_config, health_status, last_healthcheck_at, installed_at, external_id, customer_id, created_at, updated_at)
VALUES('00000000-0000-0000-2000-000000000000'::uuid, 'Sensor 2', 'SENSOR_1'::public."devicetype", '00000000-0000-2000-0000-000000000000'::uuid, 'CONNECTION'::public."componenttype", '{}'::jsonb, '{}'::jsonb, 'OK'::public."healthstatus", '2024-10-23 17:41:53.635', '2024-10-23 17:41:53.635', 'sensor_2_external_id', NULL, '2024-10-23 17:41:53.635', '2024-10-23 17:41:53.635')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.devices
(id, "name", device_type, component_id, component_type, device_specs, device_config, health_status, last_healthcheck_at, installed_at, external_id, customer_id, created_at, updated_at)
VALUES('00000000-0000-0000-3000-000000000000'::uuid, 'Sensor 3', 'EDGE'::public."devicetype", '00000000-1000-0000-0000-000000000000'::uuid, 'TRANSFORMER'::public."componenttype", '{}'::jsonb, '{}'::jsonb, 'OK'::public."healthstatus", '2024-10-23 17:41:53.635', '2024-10-23 17:41:53.635', 'sensor_2_external_id', NULL, '2024-10-23 17:41:53.635', '2024-10-23 17:41:53.635')
ON CONFLICT (id) DO NOTHING;

-- Measurements

INSERT INTO public.measurements
(id, station_id, transformer_id, connection_id, device_id, value, measurement_type, measured_at, sent_at, customer_id, created_at, updated_at)
VALUES('00000000-0000-0000-0000-000000000001'::uuid, '10000000-0000-0000-0000-000000000000'::uuid, '00000000-1000-0000-0000-000000000000'::uuid, '00000000-0000-1000-0000-000000000000'::uuid, '00000000-0000-0000-1000-000000000000'::uuid, -3.14, 'VOLTAGE'::public."measurementtype", '2024-10-23 18:46:50.853', '2024-10-23 18:56:50.853', NULL, '2024-10-23 18:59:02.510', '2024-10-23 18:59:02.510')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.measurements
(id, station_id, transformer_id, connection_id, device_id, value, measurement_type, measured_at, sent_at, customer_id, created_at, updated_at)
VALUES('00000000-0000-0000-0000-000000000002'::uuid, '10000000-0000-0000-0000-000000000000'::uuid, '00000000-1000-0000-0000-000000000000'::uuid, '00000000-0000-1000-0000-000000000000'::uuid, '00000000-0000-0000-1000-000000000000'::uuid, 1.4142, 'CURRENT'::public."measurementtype", '2024-10-23 18:46:50.853', '2024-10-23 18:56:50.853', NULL, '2024-10-23 18:59:02.510', '2024-10-23 18:59:02.510')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.measurements
(id, station_id, transformer_id, connection_id, device_id, value, measurement_type, measured_at, sent_at, customer_id, created_at, updated_at)
VALUES('00000000-0000-0000-0000-000000000003'::uuid, '10000000-0000-0000-0000-000000000000'::uuid, '00000000-1000-0000-0000-000000000000'::uuid, '00000000-0000-2000-0000-000000000000'::uuid, '00000000-0000-0000-2000-000000000000'::uuid, 2.81, 'VOLTAGE'::public."measurementtype", '2024-10-23 18:46:50.853', '2024-10-23 18:56:50.853', NULL, '2024-10-23 18:59:02.510', '2024-10-23 18:59:02.510')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.measurements
(id, station_id, transformer_id, connection_id, device_id, value, measurement_type, measured_at, sent_at, customer_id, created_at, updated_at)
VALUES('00000000-0000-0000-0000-000000000004'::uuid, '10000000-0000-0000-0000-000000000000'::uuid, '00000000-1000-0000-0000-000000000000'::uuid, NULL, '00000000-0000-0000-3000-000000000000'::uuid, 1.57, 'VOLTAGE'::public."measurementtype", '2024-10-23 18:46:50.853', '2024-10-23 18:56:50.853', NULL, '2024-10-23 18:59:02.510', '2024-10-23 18:59:02.510')
ON CONFLICT (id) DO NOTHING;
