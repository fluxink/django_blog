from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from tinymce.widgets import TinyMCE
from django import forms
from .models import PostComment, Post


class CommentCreateForm(forms.ModelForm):
    content = forms.CharField(max_length=250)

    def __init__(self, *args, **kwargs):
        super(CommentCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.template = 'blog/form_template_comment.html'
        self.helper.layout = Layout(
            Field('content', template='blog/field_comment.html'),
            Submit('submit', 'Send')
        )


    class Meta:
        model = PostComment
        fields = ['content']

class PostCreateForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80,'rows': 30,}))

    class Meta:
        model = Post
        fields = ['title', 'content']