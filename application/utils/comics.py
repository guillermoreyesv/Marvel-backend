from application.utils.marvelapi import MarvelAPI


class Comics():
    def __init__():
        return 'ok'

    def get_comics(params=''):
        response_characters = []
        order_by = 'orderBy=onsaleDate' if params else 'orderBy=title'
        response_api = MarvelAPI.make_request(
            endpoint='comics', params=params, order_by=order_by
        )

        response_json = response_api.json()

        for result in response_json['data']['results']:
            on_sale_date = Comics.get_on_sale_date(result['dates'])
            image = Comics.get_comic_image(result['images'])

            response_characters.append({
                "id": result['id'],
                "title": result['title'],
                "image": image,
                "onSaleDate": on_sale_date
            })

        return response_characters

    def get_on_sale_date(date_list=[]):
        on_sale_date = ''
        for date in date_list:
            if date['type'] == 'onsaleDate':
                on_sale_date = date['date']

        return on_sale_date

    def get_comic_image(image_list):
        image = ''
        if len(image_list):
            image = f"{image_list[0]['path']}.{image_list[0]['extension']}"
        return image
