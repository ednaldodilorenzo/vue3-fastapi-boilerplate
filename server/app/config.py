from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    echo_sql: bool = True
    test: bool = False
    project_name: str = "GesPar"
    oauth_token_secret: str = "my_dev_secret"
    debug_logs: bool = True
    app_url: str = ""
    pool_size: int = 10
    pool_timeout: int = 30


class EmailSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EMAIL_")
    password: str = ""
    username: str = "test@test.com"
    port: int = 576
    server: str = ""
    use_credentials: bool = True
    validate_certs: bool = True
    mail_starttls: bool = True
    mail_ssl_tls: bool = False


class FeatureFlagsSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FEATURE_FLAGS_")
    server_mode: bool = False
    server_key: str = ""
    source: str = ""


settings = Settings()  # type: ignore
email_settings = EmailSettings()
feature_flags_settings = FeatureFlagsSettings()
