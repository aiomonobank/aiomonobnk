from requests import Response


def is_exception(response: Response) -> bool:
    print(response.status_code)
    if response.status_code != 200:
        print(response.status_code)
        return True

    return False
