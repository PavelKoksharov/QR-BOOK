from django.db import models
from django.urls import reverse


class Books(models.Model):
    Id = models.AutoField(primary_key=True)
    BookTitle = models.CharField("Название Книги", max_length=100)
    Author = models.CharField("Автор", max_length=50, default="Неизвестен")
    Year = models.IntegerField("Год", default=0)
    Position = models.CharField("Ячейка", max_length=4, default=None, unique=True)
    Description = models.TextField("Описание", default="Простое описание")
    InfoForDocuments = models.TextField("Для ссылок в библиографический список", default="В конец")
    Free = models.BooleanField("Наличие", default=True)
    Img = models.ImageField("Img", upload_to="static/UploadImg")
    DateFirst = models.DateField("Дата начала аренды",null=True, blank=True)
    DateSecond = models.DateField("Дата возврата",null=True, blank=True)
    Reader=models.CharField("Кто взял книгу",null=True,max_length=100)

    def __str__(self):
        return self.BookTitle

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


from django.contrib.auth import get_user_model

User = get_user_model()


class Comments(models.Model):
    """Ксласс комментариев к новостям
    """
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE)
    new = models.ForeignKey(
        Books,
        verbose_name="Книга",
        on_delete=models.CASCADE)
    text = models.TextField("Комментарий")
    created = models.DateTimeField("Дата добавления", auto_now_add=True, null=True)
    moderation = models.BooleanField("Модерация", default=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return "{}".format(self.user)
