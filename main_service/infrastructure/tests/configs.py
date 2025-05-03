from contextlib import asynccontextmanager
from typing import AsyncIterator

from testcontainers.core.container import DockerContainer
from testcontainers.minio import MinioContainer
from testcontainers.postgres import PostgresContainer
from testcontainers.rabbitmq import RabbitMqContainer

from infrastructure import config
from infrastructure.mocks.providers.container import (
    create_integration_test_container,
    create_unittest_container,
)


@asynccontextmanager
async def get_container(is_intergration: bool = False):
    if is_intergration:
        async with get_containers_config() as config:
            yield create_integration_test_container(config)
    else:
        async with get_mock_config() as config:
            yield create_unittest_container(config)


@asynccontextmanager
async def get_containers_config() -> AsyncIterator[config.Config]:
    tests_config = config.get_tests_config()
    with (
        PostgresContainer(
            "postgres:17.3",
            port=tests_config.postgres_port,
            username=tests_config.postgres_user,
            password=tests_config.postgres_password,
            dbname=tests_config.postgres_db,
        ).with_exposed_ports(tests_config.postgres_port) as postgres,
        MinioContainer(
            "minio/minio:latest",
            port=tests_config.minio_root_port,
            access_key=tests_config.minio_root_user,
            secret_key=tests_config.minio_root_password,
        ).with_exposed_ports(tests_config.minio_root_port) as minio,
        RabbitMqContainer(
            "rabbitmq:3.12",
            port=tests_config.rabbitmq_port,
            username=tests_config.rabbitmq_user,
            password=tests_config.rabbitmq_password,
        ).with_exposed_ports(tests_config.rabbitmq_port) as rabbit,
        DockerContainer("greenmail/standalone:2.1.3")
        .with_exposed_ports(3025, 3143)
        .with_env(
            "GREENMAIL_OPTS",
            f"Dgreenmail.users={tests_config.imap_username}:{tests_config.imap_password}",
        ) as mail,
    ):
        tests_config.postgres_host = postgres.get_container_host_ip()
        tests_config.minio_root_host = minio.get_container_host_ip()
        tests_config.rabbitmq_host = rabbit.get_container_host_ip()
        tests_config.imap_server = f"{mail.get_container_host_ip()}:3143"
        # TODO: update smtp config

        yield tests_config


@asynccontextmanager
async def get_mock_config() -> AsyncIterator[config.Config]:
    yield config.get_mock_config()
