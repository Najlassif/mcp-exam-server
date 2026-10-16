
import hashlib
import re

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request

EMAIL = "22f3000259@ds.study.iitm.ac.in".strip().lower()

mcp = FastMCP(
    "Exam Challenge Server",
    stateless_http=True,
    json_response=True,
    streamable_http_path="/",
)

@mcp.tool()
async def solve_challenge() -> str:
    """Solve the challenge supplied in the HTTP request headers."""
    request = mcp.get_context().request_context.request

    if not isinstance(request, Request):
        raise ValueError("HTTP request is unavailable")

    challenge = request.headers.get("x-exam-challenge", "")

    if not re.fullmatch(r"[0-9a-f]{32}", challenge):
        raise ValueError("Invalid or missing challenge header")

    message = f"{challenge}:{EMAIL}"
    answer = hashlib.sha256(
        message.encode("utf-8")
    ).hexdigest()[:16]

    return answer


app = mcp.streamable_http_app()
