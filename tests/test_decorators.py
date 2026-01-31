import pytest
from httpx import Response, HTTPStatusError, RequestError
from app.utils.decorators import handle_github_api_errors

@pytest.mark.asyncio
async def test_handle_github_api_errors_success():
    @handle_github_api_errors(default_return="error")
    async def success_func():
        return "success"

    assert await success_func() == "success"

@pytest.mark.asyncio
async def test_handle_github_api_errors_404():
    @handle_github_api_errors(default_return="default")
    async def fail_404():
        response = Response(404, request=None)
        raise HTTPStatusError("Not Found", request=None, response=response)

    assert await fail_404() == "default"

@pytest.mark.asyncio
async def test_handle_github_api_errors_500():
    @handle_github_api_errors(default_return="default")
    async def fail_500():
        response = Response(500, request=None)
        raise HTTPStatusError("Internal Server Error", request=None, response=response)

    assert await fail_500() == "default"

@pytest.mark.asyncio
async def test_handle_github_api_errors_request_error():
    @handle_github_api_errors(default_return="default")
    async def fail_request():
        raise RequestError("Connection failed", request=None)

    assert await fail_request() == "default"

@pytest.mark.asyncio
async def test_handle_github_api_errors_unexpected():
    @handle_github_api_errors(default_return="default")
    async def fail_unexpected():
        raise RuntimeError("Something went wrong")

    assert await fail_unexpected() == "default"
