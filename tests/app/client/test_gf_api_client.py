from __future__ import annotations

import pytest

import genetic_forensic_portal.app.client.gf_api_client as client

TEST_FILE_DATA = b"this is a file"
TEST_METADATA = "this is metadata"


def test_upload_file_returns_uuid():
    response = client.upload_sample_analysis(TEST_FILE_DATA, TEST_METADATA)

    assert response == client.SAMPLE_UUID


def test_upload_nothing_returns_error():
    with pytest.raises(ValueError, match=client.MISSING_DATA_ERROR):
        client.upload_sample_analysis(None)  # type: ignore[arg-type]


def test_upload_no_metadata_returns_different_uuid():
    response = client.upload_sample_analysis(TEST_FILE_DATA)

    assert response == client.NO_METADATA_UUID


def test_get_scat_analysis_returns_image_path():
    response = client.get_scat_analysis(client.SAMPLE_UUID)

    assert response == client.SCAT_SAMPLE_IMAGE


def test_get_scat_analysis_no_metadata_returns_different_image_path():
    response = client.get_scat_analysis(client.NO_METADATA_UUID)

    assert response == client.SCAT_SAMPLE_IMAGE_2


def test_get_scat_analysis_raises_error():
    with pytest.raises(FileNotFoundError):
        client.get_scat_analysis("not-an-uuid")


def test_get_scat_analysis_raises_error_for_none():
    with pytest.raises(ValueError, match=client.MISSING_UUID_ERROR):
        client.get_scat_analysis(None)  # type: ignore[arg-type]


def test_list_completed_analyses_returns_list():
    response = client.list_completed_analyses()

    assert response == client.UUID_LIST
