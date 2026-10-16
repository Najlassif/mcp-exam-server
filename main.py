
import hashlib
import re

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request

EMAIL = "22f3000259@ds.study.iitm.ac.in".strip().lower()

from mcp.server.transport_security import TransportSecuritySettings

mcp = FastMCP(
    "Exam Challenge Server",
    stateless_http=True,
    json_response=True,
    streamable_http_path="/",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            "mcp-exam-server-wgqp.onrender.com",
            "mcp-exam-server-wgqp.onrender.com:*",
            "localhost:*",
            "127.0.0.1:*",
        ],
    ),
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
