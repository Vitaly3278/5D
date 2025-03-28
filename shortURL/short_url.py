from aiohttp import web
import hashlib

# Storage for shortened URLs
url_mapping = {}

async def shorten_url(request):
    # Get the URL from the request body
    data = await request.json()
    original_url = data.get('url')

    if not original_url:
        return web.Response(text="URL not provided", status=400)

    # Generate a short URL identifier
    short_url_id = hashlib.md5(original_url.encode()).hexdigest()[:6]
    url_mapping[short_url_id] = original_url

    return web.Response(text=f"Shortened URL: {short_url_id}", status=201)

async def get_original_url(request):
    short_url_id = request.match_info.get('short_url_id')

    # Find the original URL by its identifier
    original_url = url_mapping.get(short_url_id)
    if original_url:
        return web.Response(status=307, headers={'Location': original_url})
    else:
        return web.Response(text="Shortened URL not found", status=404)

app = web.Application()
app.router.add_post('/', shorten_url)
app.router.add_get('/{short_url_id}', get_original_url)

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)