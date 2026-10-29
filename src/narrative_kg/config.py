from pathlib import Path

from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str
    neo4j_password: SecretStr  # no default → required; fails loudly if missing

    pg_user: str
    pg_password: SecretStr
    pg_db: str = "narrative_kg"
    pg_host: str = "localhost"
    pg_port: str = "5432"

    @computed_field
    @property
    def pg_dsn(self) -> SecretStr:
        return SecretStr(
            f"postgresql://{self.pg_user}:{self.pg_password.get_secret_value()}"
            f"@{self.pg_host}:{self.pg_port}/{self.pg_db}"
        )

    data_dir: Path = Path("./data")


settings = Settings()
