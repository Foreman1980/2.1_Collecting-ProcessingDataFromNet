import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
from urllib.parse import urlencode
from copy import deepcopy
import json
import re


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    insta_login = 'piotrivanov850'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1595170029:AdVQAF+XIYgEcNyPUv9HKc5IxJEJujit7JkranmhB9KmhPMPOltaqovLpNVFfrqaYpZxCke6realywZGT6LMG74Evk5AUvRcBQyHIG1eidnrVpbntW+ZNS54hO1tGbiEy8nq4MSVLp9HzZUd'
    # parse_user = 'kumzhev'
    parse_user = 'p.shkolyanskiy'

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    post_hash = '15bf78a4ad24e33cbd838fdb31353ac1'
    followers_hash = 'c76146de99bb02f6415203be841dd25a'
    following_hash = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.insta_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'x-csrftoken': csrf_token},
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            yield response.follow(
                f'/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'user_name': self.parse_user},
            )

    def user_data_parse(self, response: HtmlResponse, user_name):
        user_id = self.fetch_user_id(response.text, user_name)

        # Парсим список подписчиков
        var_followers = {'id': user_id,
                         'include_reel': True,
                         # 'fetch_mutual': True, # всё работает и без этого параметра
                         'first': 24,
                         }
        url_followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(var_followers)}'
        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={'user_name': user_name, 'var_followers': deepcopy(var_followers)}
        )

        # Парсим список тех, на кого подписан пользователь
        var_following = {'id': user_id,
                         'include_reel': True,
                         # 'fetch_mutual': False, # всё работает и без этого параметра
                         'first': 24,
                         }
        url_following = f'{self.graphql_url}query_hash={self.following_hash}&{urlencode(var_following)}'
        yield response.follow(
            url_following,
            callback=self.user_following_parse,
            cb_kwargs={'user_name': user_name, 'var_following': deepcopy(var_following)}
        )

    def user_followers_parse(self, response: HtmlResponse, user_name, var_followers):
        j_data = json.loads(response.text)
        if j_data['status'] == 'ok':
            page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
            if page_info.get('has_next_page'):
                var_followers['after'] = page_info.get('end_cursor')
                var_followers['first'] = 12
                url_followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(var_followers)}'
                yield response.follow(
                    url_followers,
                    callback=self.user_followers_parse,
                    cb_kwargs={'user_name': user_name, 'var_followers': deepcopy(var_followers)}
                )
        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for user in followers:
            yield InstaparserItem(
                user_name=user.get('node').get('username'),
                full_name=user.get('node').get('full_name'),
                user_id=user.get('node').get('id'),
                profil_pic_url=user.get('node').get('profile_pic_url'),
                following=[user_name],
                followers=[],
            )

    def user_following_parse(self, response: HtmlResponse, user_name, var_following):
        j_data = json.loads(response.text)
        if j_data['status'] == 'ok':
            page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
            if page_info.get('has_next_page'):
                var_following['after'] = page_info.get('end_cursor')
                var_following['first'] = 12
                url_following = f'{self.graphql_url}query_hash={self.following_hash}&{urlencode(var_following)}'
                yield response.follow(
                    url_following,
                    callback=self.user_following_parse,
                    cb_kwargs={'user_name': user_name, 'var_following': deepcopy(var_following)}
                )
        following = j_data.get('data').get('user').get('edge_follow').get('edges')
        for user in following:
            yield InstaparserItem(
                user_name=user.get('node').get('username'),
                full_name=user.get('node').get('full_name'),
                user_id=user.get('node').get('id'),
                profil_pic_url=user.get('node').get('profile_pic_url'),
                following=[],
                followers=[user_name],
            )

    def fetch_csrf_token(self, page_http: str) -> str:
        pattern = re.compile('\"csrf_token\":\"\\w+\"')
        return re.search(pattern, page_http).group().split(':').pop().strip('"')

    def fetch_user_id(self, page_http: str, user_name: str) -> str:
        pattern = re.compile(f'\"id\":\"\\d+\",\"username\":\"{user_name}\"')
        return re.search(pattern, page_http).group().split(',')[0].split(':').pop().strip('"')
