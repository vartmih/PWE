import pytest
from alembic.command import upgrade, downgrade
from alembic.config import Config
from alembic.script import ScriptDirectory, Script

from pwe.utils import get_alembic_config_from_db_url


def get_revisions():
    """
    Получает и сортирует список миграций

    :return: отсортированный список миграций
    """
    # конфигурация Alembic
    config = get_alembic_config_from_db_url()

    # директория с миграциями Alembic
    revisions_dir = ScriptDirectory.from_config(config)

    # Отсортированный список миграций
    revisions = list(revisions_dir.walk_revisions('base', 'head'))
    revisions.reverse()

    return revisions


@pytest.mark.parametrize('revision', get_revisions())
def test_migrations_stairway(alembic_config: Config, revision: Script) -> None:
    """
    Ступенчатое тестирование миграций

    Parameters:
        alembic_config: конфигурация Alembic
        revision: миграция

    :return:
    """
    upgrade(alembic_config, revision.revision)

    # Если миграция первая, то откатываемся полностью ('base')
    downgrade(alembic_config, revision.down_revision or 'base')
    upgrade(alembic_config, revision.revision)
