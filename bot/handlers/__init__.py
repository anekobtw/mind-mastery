from aiogram import Router


def get_handlers_router() -> Router:
    from . import common, notes, quote, uptime, wiki

    router = Router()
    router.include_router(common.router)
    router.include_router(notes.router)
    router.include_router(quote.router)
    router.include_router(uptime.router)
    router.include_router(wiki.router)

    return router
