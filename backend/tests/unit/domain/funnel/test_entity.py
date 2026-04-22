import uuid

import pytest

from src.backend.domain.funnel.entity import Funnel, FunnelStage
from src.backend.domain.funnel.value_objects.probability.value_object import Probability
from src.backend.domain.shared.value_objects.hex.value_object import HexCode
from src.backend.domain.shared.value_objects.name.value_object import Name
from tests.unit.domain.funnel.value_objects.test_probability import win_probability
from tests.unit.domain.shared.value_objects.test_hex import hex_code
from tests.unit.domain.shared.value_objects.test_name import test_name


@pytest.fixture
def funnel_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture
def valid_funnel(
        funnel_id,
        test_name,
) -> Funnel:
    return Funnel(
        id=funnel_id,
        name=test_name,
        is_deleted=False,
    )

def test_valid_create_funnel(
        funnel_id: uuid.UUID,
        test_name: Name,
) -> None:
    funnel=Funnel.create(
        id=funnel_id,
        name=test_name.value,
    )
    assert funnel.id == funnel_id
    assert funnel.name == test_name
    assert funnel.is_deleted == False


def test_delete_funnel(
        valid_funnel
) -> None:
    valid_funnel.delete()
    assert valid_funnel.is_deleted == True


@pytest.fixture
def funnel_stage_id() -> uuid.UUID:
    return uuid.uuid4()

@pytest.fixture
def funnel_stage_order():
    return 2


@pytest.fixture
def valid_funnel_stage(
        funnel_stage_id,
        funnel_id,
        test_name,
        hex_code,
        win_probability,
        funnel_stage_order,
) -> FunnelStage:
    return FunnelStage(
        id=funnel_stage_id,
        funnel_id=funnel_id,
        name=test_name,
        win_probability=win_probability,
        hex=hex_code,
        order=funnel_stage_order
    )

def test_valid_create_funnel_stage(
        funnel_stage_id: uuid.UUID,
        test_name: Name,
        funnel_id: uuid.UUID,
        hex_code: HexCode,
        win_probability: Probability,
        funnel_stage_order: int
) -> None:
    funnel_stage=FunnelStage.create(
        id=funnel_stage_id,
        funnel_id=funnel_id,
        name=test_name.value,
        win_probability=win_probability.value,
        hex=hex_code.value,
        order=funnel_stage_order
    )
    assert funnel_stage.id == funnel_stage_id
    assert funnel_stage.funnel_id == funnel_id
    assert funnel_stage.name == test_name
    assert funnel_stage.win_probability == win_probability
    assert funnel_stage.hex == hex_code
    assert funnel_stage.order == funnel_stage_order

