from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone = PhoneNumberField(verbose_name=_("Номер телефона"), blank=True, null=True)
    raw_password = models.CharField(
        verbose_name=_("Сырой пароль"), max_length=255, blank=True, null=True
    )
    is_mentor = models.BooleanField(verbose_name=_("Ментор"), default=False)
    mentor = models.ForeignKey(
        "users.User",
        verbose_name=_("Ментор"),
        on_delete=models.SET_NULL,
        related_name="students",
        null=True,
    )

    def __str__(self):
        return f"{self.username} {self.email} {self.phone}"

    class Meta:
        ordering = ("id",)
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
