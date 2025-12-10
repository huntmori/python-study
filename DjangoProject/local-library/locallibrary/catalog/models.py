from django.db import models
from django.urls import reverse


# Create your models here.
class MyModelName(models.Model):

    #Fields
    """
        help_text = html from 에대해 텍스트 라벨 제공
        verbose_name = 필드 라발안에서 사용되는 인간이 읽을 수 있는 필드이름.
        default = 필드를 위한 기본 값 또는 호출 가능한 객체. 객체일 경우 새로운 레코드가 생성 될 떄 마다 호출
        null = 만약 True라면, 장고는 빈 NULL 값을 데이터베이스에 저장.(CharField는 빈 문자열을 저장)
                기본값은 False
        blank = 만약 True라면 from 안에 비워두는것이 허락됨. 기본값은 False
        choices : 필드를 위한 선택들의 모임. 이 인수가 제공되면 form은 선택상자가 됨
        primary_key = 만약 True라면, 현재 필드를 모델의 primary key로 설정
                    지정된 필드가 없다면 장고가 자동적으로 이 목적의 필드를 추가함

        models 필드 유형
            CharField,
            TextField,
            IntegerField,
            DateField, DateTimeField,
            EmailField,
            FileField, ImageField
            AutoField,
            ForeignKey
            ManyToManyField
    """
    my_field_name = models.CharField(
        max_length=20,
        help_text='Enter field documentation'
    )

    # Meta Data
    class Meta:
        ordering = ['-my_field_name']

    # Methods
    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.my_field_name

class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Enter a book genre (e.g. Science Fiction)'
    )

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        null=True)

    summary = models.TextField(
        max_length=1000,
        help_text='Enter a brief description of the book'
    )
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        unique=True,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

