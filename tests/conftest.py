

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from dataclasses import dataclass

import pytest

from app.service import create_server


@dataclass
class Response:
    

    status: int
    body: str
    content_type: str | None

    def json(self):
        return json.loads(self.body)


@pytest.fixture(scope="session")
def base_url():
   
    server = create_server(port=0, host="127.0.0.1")
    host, port = server.server_address[:2]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.fixture
def http_get(base_url):
    

    def _get(path: str) -> Response:
        url = f"{base_url}{path}"
        try:
            with urllib.request.urlopen(url, timeout=5) as resp: 
                raw = resp.read().decode("utf-8")
                return Response(resp.status, raw, resp.headers.get("Content-Type"))
        except urllib.error.HTTPError as exc:  
            raw = exc.read().decode("utf-8")
            return Response(exc.code, raw, exc.headers.get("Content-Type"))

    return _get
