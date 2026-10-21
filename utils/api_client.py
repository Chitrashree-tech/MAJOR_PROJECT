import requests


API_URL = "http://127.0.0.1:8000"


def api_get(endpoint, params=None):
    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            params=params,
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        return {
            "error": str(e)
        }


def api_post(endpoint, data=None):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=data,
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        return {
            "error": str(e)
        }


def check_backend():
    result = api_get("/health")

    return (
        result.get("status") == "healthy"
        if isinstance(result, dict)
        else False
    )