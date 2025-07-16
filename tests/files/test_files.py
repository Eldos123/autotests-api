from http import HTTPStatus

import pytest

from clients.files.files_client import FilesClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.files import assert_create_file_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.files
@pytest.mark.regression
class TestFiles:
    def test_create_file(self, files_client: FilesClient):
        request = CreateFileRequestSchema(upload_file="./testdata/files/image.png")
        response = files_client.create_file_api(request)
        response_data = CreateFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_file_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())