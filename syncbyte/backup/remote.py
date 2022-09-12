import os
import logging
import gzip
import subprocess

import boto3

from syncbyte.constant import DBType
from syncbyte.exceptions import NotSupport, DumpFailed
from syncbyte.config import settings

logger = logging.getLogger(__name__)

CACHE_VOLUME = settings.CACHE_VOLUME
HOST_PATH = settings.HOST_PATH
IS_LOCAL_DUMP = settings.IS_LOCAL_DUMP


def gen_desc_file(dataset_name):
    return f"{dataset_name}.sql"


def compress_file(src_file):
    cfile = f"{src_file}.gz"
    
    with open(src_file, 'rb') as f_in:
        with gzip.open(cfile, 'wb') as f_out:
            for line in f_in:
                f_out.write(line)
    
    os.remove(src_file)
    return cfile


class DatabaseResource:
    def __init__(self, name, db_type, host, port, user, password, dbname, db_version):
        self.name = name
        self.db_type = db_type
        self.host = host
        self.port = port
        self.user = user
        self.password= password
        self.dbname = dbname
        self.db_version = db_version

    def _gen_dump_command(self, dest_file, is_local_dump=True):
        command = None
        _, file_name = os.path.split(dest_file)

        if self.db_type == DBType.PostgreSQL:
            if is_local_dump is True:
                command = f"pg_dump --dbname='postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}' -Fc -f {dest_file}"
            else:
                uid = os.getuid()
                gid = os.getgid()

                command = f"""sudo chmod -R o+w {CACHE_VOLUME}; sudo docker run --rm -v {HOST_PATH}:/opt:rw postgres:{self.db_version} bash -c 'pg_dump postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname} -Fc -f /opt/{file_name};chmod -R g+w /opt;chown {uid}:{gid} /opt/{file_name}'"""
        else:
            raise NotSupport(f"not support db type {self.db_type}")

        return command

    def dump(self, dataset_name):
        dest_file = os.path.join(CACHE_VOLUME, gen_desc_file(dataset_name))

        c = self._gen_dump_command(dest_file, is_local_dump=IS_LOCAL_DUMP)
        
        logger.debug(f"run command: {c}")
        cmd = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE)
        cmd.communicate()

        logger.debug(f"run result: {cmd.returncode}")
        if int(cmd.returncode) != 0:
            err = f"dump resource {self.name} failed"
            logger.error(err)
            raise DumpFailed(err)
        
        return dest_file


class S3:
    def __init__(self, endpoint, access_key, secret_key, bucket):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket

    def upload(self, file):
        s3 = boto3.resource(
            "s3", 
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )

        _, obj_name = os.path.split(file)
        s3.Bucket(self.bucket).upload_file(file, obj_name)


def remote_backup(dataset_name, db_options, st_options):
    resource = DatabaseResource(
        db_options["name"],
        db_options["db_type"],
        db_options["host"],
        db_options["port"],
        db_options["user"],
        db_options["password"],
        db_options["dbname"],
        db_options["db_version"],
    )

    storage = S3(
        st_options["endpoint"],
        st_options["access_key"],
        st_options["secret_key"],
        st_options["bucket"],
    )

    dest_file = resource.dump(dataset_name)
    logger.info(f"dump completed, dest_file: {dest_file}")

    comp_file = compress_file(dest_file)
    logger.info(f"compress file, filename: {comp_file}")

    storage.upload(comp_file)
    logger.info(f"upload completed")

    os.remove(comp_file)
