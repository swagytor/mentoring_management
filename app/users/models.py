from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone = PhoneNumberField(verbose_name=_("Номер телефона"), blank=True, null=True)

    def __str__(self):
        return f"{self.username} {self.email} {self.phone}"

    class Meta:
        ordering = ("id",)
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
