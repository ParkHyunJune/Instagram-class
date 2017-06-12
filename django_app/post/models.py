# # shift + Command + F : 프로젝트내에서 모두 찾기
# In [1]: u = User.objects.create_user('phj')
#
# In [2]: u.set_password('qkrguswns')
#
# In [3]: u.save()
#
# In [4]: p1 = Post.objects.create(author=u)
#
# In [5]: p1
# Out[5]: <Post: Post object>
#
# In [6]: u2 = User.objects.create_user('lsj')
#
# In [7]: u2.first_name = '수진'
#
# In [8]: u2.last_name = '이'
#
# In [9]: u2.save()
#
# In [10]: u.post_set.all()
# Out[10]: <QuerySet [<Post: Post object>]>
#
# In [11]: p1.comment_set.create(author=u2, content='댓글을달자')
# Out[11]: <Comment: Comment object>
#
# In [12]: Comment.objects.create(post=p1, author=u2, content='댓글을 다시 달자')
# Out[12]: <Comment: Comment object>≤

from django.db import models
from django.conf import settings

class Post(models.Model):
    # Django가 제공하는 기본 User와 연결되도록 수정
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_posts',
        through='PostLike',
    )
    tags = models.ManyToManyField('Tag')

    def add_comment(self, user, content):
        # 자신을 post로 갖고, 전달받은 user를 author로 가지며
        # content를 content필드내용으로 넣는 Comment객체 생성
        return self.comment_set.create(author=user, content=content)

    def add_tag(self, tag_name):
        # tags에 tag매개변수로 전달된 값(str)을
        # name으로 갖는 Tag객체를 (이미 존재하면)가져오고 없으면 생성하여
        # 자신의 tags에 추가
        tag, tag_created = Tag.objects.get_or_create(name=tag_name)
        if not self.tags.filter(id=tag.id).exists():
            self.tags.add(tag)

    @property
    def like_count(self):
        # 자신을 like하고 있는 user수 리턴
        return self.like_users.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CommentLike',
        related_name='like_comments',
    )


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Tag({})'.format(self.name)