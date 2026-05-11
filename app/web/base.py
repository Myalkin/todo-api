from aiohttp.web import View as AiohttpView, Request as AiohttpRequest


class Request(AiohttpRequest):
    pass


class View(AiohttpView):
    request: Request