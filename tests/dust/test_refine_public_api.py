import torch


def test_public_api_exposes_semantic_name_and_legacy_alias():
    from methods.refine_tracking import NDS, RefinePostprocessor

    assert NDS is RefinePostprocessor


def test_public_postprocessor_preserves_first_frame_detections():
    from methods.refine_tracking import RefinePostprocessor

    detections = torch.tensor(
        [[0, 0, 10, 10, 0.9, 0], [1, 1, 5, 5, 0.8, 1]],
        dtype=torch.float32,
    )

    refined = RefinePostprocessor().refine_box(detections, update_class_id=0)

    assert torch.equal(refined, detections)
