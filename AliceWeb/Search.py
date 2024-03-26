import aiohttp

class AliceSearch:
    def __init__(self, url: str):
        """
        Initializes the class instance with the provided URL.

        Parameters:
            url (str): The URL to be assigned to the instance.

        Returns:
            None
        """
        self.url = url
        self.clientsession = aiohttp.ClientSession()
        
    async def search_with_searxng(self, query, categories=None, engines=None, language=None, page=1, time_range=None, format=None, results_on_new_tab=None, image_proxy=None, autocomplete=None, safesearch=None, theme=None, enabled_plugins=None, disabled_plugins=None, enabled_engines=None, disabled_engines=None):
        """
        Asynchronously performs a search using the searxng API.

        Args:
            query (str): The search query.
            categories (str, optional): The categories to search in. Defaults to None.
            engines (str, optional): The search engines to use. Defaults to None.
            language (str, optional): The language of the search results. Defaults to None.
            page (int, optional): The page number of the search results. Defaults to 1.
            time_range (str, optional): The time range of the search results. Defaults to None.
            format (str, optional): The format of the search results. Defaults to None.
            results_on_new_tab (bool, optional): Whether to open search results in a new tab. Defaults to None.
            image_proxy (str, optional): The URL of the image proxy. Defaults to None.
            autocomplete (bool, optional): Whether to enable autocomplete. Defaults to None.
            safesearch (str, optional): The safesearch mode. Defaults to None.
            theme (str, optional): The theme of the search results. Defaults to None.
            enabled_plugins (str, optional): The enabled plugins. Defaults to None.
            disabled_plugins (str, optional): The disabled plugins. Defaults to None.
            enabled_engines (str, optional): The enabled search engines. Defaults to None.
            disabled_engines (str, optional): The disabled search engines. Defaults to None.

        Returns:
            dict: The JSON response containing the search results.
        """
        params = {'q': query}
        # Optional parameters
        if categories is not None:
            params['categories'] = categories
        if engines is not None:
            params['engines'] = engines
        if language is not None:
            params['language'] = language
        if page is not None:
            params['page'] = page
        if time_range is not None:
            params['time_range'] = time_range
        if format is not None:
            params['format'] = format
        if results_on_new_tab is not None:
            params['results_on_new_tab'] = results_on_new_tab
        if image_proxy is not None:
            params['image_proxy'] = image_proxy
        if autocomplete is not None:
            params['autocomplete'] = autocomplete
        if safesearch is not None:
            params['safesearch'] = safesearch
        if theme is not None:
            params['theme'] = theme
        if enabled_plugins is not None:
            params['enabled_plugins'] = enabled_plugins
        if disabled_plugins is not None:
            params['disabled_plugins'] = disabled_plugins
        if enabled_engines is not None:
            params['enabled_engines'] = enabled_engines
        if disabled_engines is not None:
            params['disabled_engines'] = disabled_engines

        async with self.clientsession as session:
            async with session.get(self.url, params=params) as response:
                return await response.json()