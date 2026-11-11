from backend.application.funnel.error import StageNotFunnelError
from src.backend.domain.funnel.entity import FunnelStage


class FunnelStageOrderingServices:
    def __sort(
            self,
            stages: list[FunnelStage]
    )  -> list[FunnelStage]:
        sorted_stages = sorted(stages, key=lambda s: s.order)
        return sorted_stages

    def normalize(
            self,
            stages: list[FunnelStage]
    ) -> list[FunnelStage]:
        sorted_stages = self.__sort(stages)
        for idx, stage in enumerate(sorted_stages):
            if idx != stage.order:
                stage.change_order(idx)
        return sorted_stages

    def insert(
            self,
            stages: list[FunnelStage],
            new_stage: FunnelStage,
            position: int
    ):
        sorted_stages = self.__sort(stages)
        position = max(0, min(position, len(sorted_stages)))
        sorted_stages.insert(position, new_stage)
        for idx, stage in enumerate(sorted_stages):
            stage.change_order(idx)
        return sorted_stages

    def move(
            self,
            stages: list[FunnelStage],
            stage: FunnelStage,
            new_position: int
    ):
        sorted_stages = self.__sort(stages)
        moving = next(
            (s for s in sorted_stages if s == stage),
            None
        )
        if not moving:
            raise StageNotFunnelError()
        sorted_stages.remove(moving)
        return self.insert(sorted_stages, stage, new_position)

    def remove(
            self,
            stages: list[FunnelStage],
            stage: FunnelStage,
    ):
        remaining = [s for s in stages if s != stage]
        return self.normalize(remaining)