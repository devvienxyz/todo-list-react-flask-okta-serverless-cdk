from application import application as app


def lambda_handler(event, context):
    method = event.get("httpMethod")
    path = event.get("path")
    headers = event.get("headers", {})
    body = event.get("body", None)
    query_string = event.get("queryStringParameters", {})
    status_headers = {}
    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": "&".join(
            [f"{key}={value}" for key, value in query_string.items()]
        ),
        "CONTENT_TYPE": headers.get("Content-Type", ""),
        "wsgi.input": body,
        "wsgi.url_scheme": (
            "https"
            if event.get("requestContext", {}).get("protocol", "").startswith("HTTPS")
            else "http"
        ),
        "SERVER_NAME": headers.get("Host", ""),
        "REMOTE_ADDR": event.get("requestContext", {})
        .get("identity", {})
        .get("sourceIp", ""),
        "wsgi.errors": context.log_stream_name,
        "lambda.event": event,
        "lambda.context": context,
    }

    def start_response(status, response_headers):
        status_headers["status"] = int(status.split()[0])
        status_headers["headers"] = dict(response_headers)

    with app.app_context():
        response = app(environ, start_response)

    response_body = b"".join(response).decode("utf-8")

    return {
        "statusCode": status_headers["status"],
        "body": response_body,
        "headers": status_headers["headers"],
    }
