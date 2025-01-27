from dagster import Definitions, load_assets_from_modules

from ec_prediction.assets import assets, metrics  # noqa: TID252

all_assets = load_assets_from_modules([assets])

metric_assets = load_assets_from_modules([metrics])

defs = Definitions(
    assets=[*all_assets, *metric_assets]
)
