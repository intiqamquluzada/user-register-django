import random
import string
from typing import Any


class Generator:

    @staticmethod
    def code_slug_generator(size: str, chars: Any):
        return "".join(random.choice(chars) for _ in range(size))

    @classmethod
    def create_slug_shortcode(cls, size: str, model_: Any) -> str:
        new_code = cls.code_slug_generator(
            size=size, chars=string.digits + string.ascii_letters
        )
        qs_exists = model_.objects.filter(slug=new_code).exists()
        if qs_exists:
            return cls.create_slug_shortcode(size, model_)
        return new_code

    @classmethod
    def create_activation_code(cls, size: str, model_: Any) -> str:
        new_code = cls.code_slug_generator(
            size=size, chars=string.digits
        )
        qs_exists = model_.objects.filter(activation_code=new_code).exists()
        if qs_exists:
            return cls.create_slug_shortcode(size, model_)
        return new_code

    @classmethod
    def create_reset_code(cls, size: str, model_: Any) -> str:
        new_code = cls.code_slug_generator(
            size=size, chars=string.digits
        )
        qs_exists = model_.objects.filter(password_reset_code=new_code).exists()
        if qs_exists:
            return cls.create_slug_shortcode(size, model_)
        return new_code