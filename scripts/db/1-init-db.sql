BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 33abe6f320cc

CREATE TABLE resource (
    id SERIAL NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    deleted BOOLEAN, 
    name VARCHAR(60), 
    uri VARCHAR(200), 
    PRIMARY KEY (id)
);

CREATE TABLE sync_job (
    id SERIAL NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    deleted BOOLEAN, 
    status VARCHAR(20), 
    PRIMARY KEY (id)
);

INSERT INTO alembic_version (version_num) VALUES ('33abe6f320cc') RETURNING alembic_version.version_num;

-- Running upgrade 33abe6f320cc -> ca8c4b92c218

ALTER TABLE resource ADD COLUMN db_type VARCHAR(20);

ALTER TABLE resource ADD COLUMN db_version VARCHAR(60);

ALTER TABLE resource ADD COLUMN host VARCHAR(60);

ALTER TABLE resource ADD COLUMN port INTEGER;

ALTER TABLE resource ADD COLUMN "user" VARCHAR(60);

ALTER TABLE resource ADD COLUMN password VARCHAR(500);

ALTER TABLE resource ADD COLUMN dbname VARCHAR(100);

ALTER TABLE resource ADD COLUMN args VARCHAR(600);

ALTER TABLE resource DROP COLUMN uri;

UPDATE alembic_version SET version_num='ca8c4b92c218' WHERE alembic_version.version_num = '33abe6f320cc';

-- Running upgrade ca8c4b92c218 -> 80d7aa98ca72

CREATE TABLE s3 (
    id SERIAL NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    deleted BOOLEAN, 
    endpoint VARCHAR(60), 
    access_key VARCHAR(200), 
    secret_key VARCHAR(200), 
    bucket_name VARCHAR(120), 
    type VARCHAR(30), 
    PRIMARY KEY (id)
);

UPDATE alembic_version SET version_num='80d7aa98ca72' WHERE alembic_version.version_num = 'ca8c4b92c218';

-- Running upgrade 80d7aa98ca72 -> b07c3f9ccb5f

CREATE TABLE backup_job (
    id SERIAL NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    deleted BOOLEAN, 
    start_time TIMESTAMP WITHOUT TIME ZONE, 
    end_time TIMESTAMP WITHOUT TIME ZONE, 
    size INTEGER, 
    is_valid BOOLEAN, 
    status VARCHAR(20), 
    resource_id INTEGER, 
    storage_id INTEGER, 
    dataset_name VARCHAR(200), 
    PRIMARY KEY (id)
);

DROP TABLE sync_job;

UPDATE alembic_version SET version_num='b07c3f9ccb5f' WHERE alembic_version.version_num = '80d7aa98ca72';

COMMIT;

