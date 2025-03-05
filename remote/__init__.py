from js import document


async def main():
    # from wwwpy.remote import shoelace
    # shoelace.setup_shoelace()
    document.head.insertAdjacentHTML('beforeend', _style)
    from . import main_component  # for component registration
    document.body.innerHTML = '<component-1></component-1>'



# language=html
_style = """
<meta name="viewport" content="width=device-width, initial-scale=3.0">
<style>
    body {
        background: #121212;
        color: #e0e0e0;
        margin: 1rem;
        font: 16px sans-serif;
    }

    a {
        color: #bb86fc
    }
</style>
"""
