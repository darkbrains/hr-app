import sys
from hashlib import sha1, md5
from collections import OrderedDict
if sys.version_info.major > 2:
    from urllib.parse import urlencode
else:
    from urllib import urlencode
import hmac
import requests
import base64


phone_verification_texts = {
    'en': {
        'message': "Your verification code is: "
    },
    'ru': {
        'message': "Ваш код верификаци: "
    },
    'hy': {
        'message': "Ձեր նույնականացման կոդն է՝ "
    }
}

phone_contents = {
    'en': {
        'rejection_subject': "Thank You for Your Participation",
        'rejection_message': (
            "Thank you for your time and patience throughout the interview process.\n\n"
            "We regret to inform you that your result did not qualify for the next stage of the interview process.\n\n"
            "We wish you all the best in your future endeavors.\n\n"
            "Best regards\nThe People Connect Team"
        ),
        'invitation_subject': "Congratulations - Next Steps in People Connect",
        'invitation_message': (
            "Congratulations on successfully passing the initial screening!\n\n"
            "We are pleased to invite you to the next stage of the interview.\n\n"
            "We will inform you about further actions within 2 business days.\n\n"
            "Best regards\nThe People Connect Team"
        )
    },
    'ru': {
        'rejection_subject': "Спасибо за ваше участие",
        'rejection_message': (
            "Благодарим вас за время и терпение в течение всего процесса собеседования.\n\n"
            "К сожалению, мы должны сообщить, что вы не прошли в следующий этап процесса собеседования.\n\n"
            "Желаем вам всего наилучшего в вашей дальнейшей деятельности.\n\n"
            "С уважением\nКоманда People Connect"
        ),
        'invitation_subject': "Поздравляем - Следующие шаги в People Connect",
        'invitation_message': (
            "Поздравляем с успешным прохождением начального отбора!\n\n"
            "Мы рады пригласить вас на следующий этап собеседования.\n\n"
            "сообщим вам о дальнейших действиях в течение 2 рабочих дней.\n\n"
            "С уважением\nКоманда People Connect"
        )
    },
    'hy': {
        'rejection_subject': "Շնորհակալություն մասնակցության համար",
        'rejection_message': (
            "Շնորհակալություն հարցազրույցի ողջ ընթացքում ձեր ժամանակի և համբերության համար:\n\n"
            "Ցավոք, մենք պետք է տեղեկացնենք, որ դուք չեք անցել հարցազրույցի հաջորդ փուլ:\n\n"
            "Մաղթում ենք ձեզ ամենայն բարիք ձեր հետագա գործունեության մեջ։\n\n"
            "Հարգանքով`\nPeople Connect թիմը"
        ),
        'invitation_subject': "Շնորհակալություն մասնակցության համար - Հաջորդ քայլերը People Connect-ում",
        'invitation_message': (
            "Շնորհավորում ենք նախնական հարցազրույցի հաջող ավարտի կապակցությամբ:\n\n"
            "Մենք ուրախ ենք Ձեզ հրավիրել հարցազրույցի հաջորդ փուլ։\n\n"
            "Մենք ձեզ կտեղեկացնենք հետագա գործողությունների մասին 2 աշխատանքային օրվա ընթացքում:\n\n"
            "Հարգանքով`\nPeople Connect թիմը"
        )
    }
}


class ZadarmaAPI(object):

    def __init__(self, key, secret, is_sandbox=False):
        """
        Constructor
        :param key: key from personal
        :param secret: secret from personal
        :param is_sandbox: (True|False)
        """
        self.key = key
        self.secret = secret
        self.is_sandbox = is_sandbox
        self.__url_api = 'https://api.zadarma.com'
        if is_sandbox:
            self.__url_api = 'https://api-sandbox.zadarma.com'

    def call(self, method, params={}, request_type='GET', format='json', is_auth=True):
        """
        Function for send API request
        :param method: API method, including version number
        :param params: Query params
        :param request_type: (get|post|put|delete)
        :param format: (json|xml)
        :param is_auth: (True|False)
        :return: response
        """
        request_type = request_type.upper()
        if request_type not in ['GET', 'POST', 'PUT', 'DELETE']:
            request_type = 'GET'
        params['format'] = format
        auth_str = None
        is_nested_data = False
        for k in params.values():
            if not isinstance(k, str):
                is_nested_data = True
                break
        if is_nested_data:
            params_string = self.__http_build_query(OrderedDict(sorted(params.items())))
            params = params_string
        else:
            params_string = urlencode(OrderedDict(sorted(params.items())))

        if is_auth:
            auth_str = self.__get_auth_string_for_header(method, params_string)

        if request_type == 'GET':
            result = requests.get(self.__url_api + method + '?' + params_string, headers={'Authorization': auth_str})
        elif request_type == 'POST':
            result = requests.post(self.__url_api + method, headers={'Authorization': auth_str}, data=params)
        elif request_type == 'PUT':
            result = requests.put(self.__url_api + method, headers={'Authorization': auth_str}, data=params)
        elif request_type == 'DELETE':
            result = requests.delete(self.__url_api + method, headers={'Authorization': auth_str}, data=params)
        return result.text

    def __http_build_query(self, data):
        parents = list()
        pairs = dict()

        def renderKey(parents):
            depth, outStr = 0, ''
            for x in parents:
                s = "[%s]" if depth > 0 or isinstance(x, int) else "%s"
                outStr += s % str(x)
                depth += 1
            return outStr

        def r_urlencode(data):
            if isinstance(data, list) or isinstance(data, tuple):
                for i in range(len(data)):
                    parents.append(i)
                    r_urlencode(data[i])
                    parents.pop()
            elif isinstance(data, dict):
                for key, value in data.items():
                    parents.append(key)
                    r_urlencode(value)
                    parents.pop()
            else:
                pairs[renderKey(parents)] = str(data)

            return pairs
        return urlencode(r_urlencode(data))

    def __get_auth_string_for_header(self, method, params_string):
        """
        :param method: API method, including version number
        :param params: Query params dict
        :return: auth header
        """
        data = method + params_string + md5(params_string.encode('utf8')).hexdigest()
        hmac_h = hmac.new(self.secret.encode('utf8'), data.encode('utf8'), sha1)
        if sys.version_info.major > 2:
            bts = bytes(hmac_h.hexdigest(), 'utf8')
        else:
            bts = bytes(hmac_h.hexdigest()).encode('utf8')
        auth = self.key + ':' + base64.b64encode(bts).decode()
        return auth

    def send_sms(self, phone_number, message, sender="People Connect Team", language=None):
        """
        Send an SMS message using Zadarma API.
        :param phone_number: The recipient phone number
        :param message: The SMS message content
        :param sender: (Optional) Sender ID (registered in Zadarma)
        :param language: (Optional) Template language
        """
        method = '/v1/sms/send/'
        params = {
            'number': phone_number,
            'message': message
        }
        if sender:
            params['sender'] = sender
        if language:
            params['language'] = language

        return self.call(method, params=params, request_type='POST')

    def send_verification_code(self, phone_number, code, language='en'):
        """
        Send a verification code SMS.
        :param phone_number: The recipient's phone number
        :param code: Verification code to send
        :param language: Language of the message template
        """
        message = f"{phone_verification_texts[language]['message']} {code}"
        return self.send_sms(phone_number, message)

    def send_rejection_message(self, phone_number, language='en'):
        """
        Send a rejection message to the specified phone number in the selected language.
        :param phone_number: The recipient's phone number
        :param language: Language of the message template
        """
        rejection_info = phone_contents[language]['rejection_message']
        return self.send_sms(phone_number, rejection_info)

    def send_invitation_message(self, phone_number, language='en'):
        """
        Send an invitation message to the specified phone number in the selected language.
        :param phone_number: The recipient's phone number
        :param language: Language of the message template
        """
        invitation_info = phone_contents[language]['invitation_message']
        return self.send_sms(phone_number, invitation_info)
