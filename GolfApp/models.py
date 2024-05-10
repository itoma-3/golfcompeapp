from django.db import models

class Participant(models.Model):
    name = models.CharField(max_length=100)
    kana_name = models.CharField(max_length=100, verbose_name='氏名カナ',default='')  # 氏名カナを追加
    average_score = models.IntegerField(default=0)  # FloatFieldからIntegerFieldに変更
    gender = models.CharField(max_length=1, choices=(('M', '男'), ('F', '女')))
    email = models.EmailField(max_length=254, verbose_name='メールアドレス', default='',blank=True)
    transportation = models.CharField(max_length=2, choices=(('Y', 'あり'), ('N', 'なし')), verbose_name='移動手段',default='N',blank=True)  # 移動手段を追加
    postal_code = models.CharField(max_length=8, verbose_name='郵便番号', default='',blank=True)  # 郵便番号
    prefecture = models.CharField(max_length=100, verbose_name='都道府県', default='',blank=True)  # 都道府県
    city = models.CharField(max_length=100, verbose_name='市区町村', default='',blank=True)  # 市区町村
    address = models.CharField(max_length=255, verbose_name='番地', default='',blank=True)  # 番地
    building = models.CharField(max_length=255, verbose_name='建物名', default='', blank=True)  # 建物名（任意）

    def __str__(self):
        return self.name
    
class GroupingResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # その他、組分けに使用した条件などを保存するフィールド
    

class Group(models.Model):
    result = models.ForeignKey(GroupingResult, related_name='groups', on_delete=models.CASCADE)
    participants = models.ManyToManyField(Participant)

    def __str__(self):
        return f"Group {self.id} of {self.result.id}"
    