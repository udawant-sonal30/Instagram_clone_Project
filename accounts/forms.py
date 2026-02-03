from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Post
from .models import Comment
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom error messages
        self.fields['password1'].help_text = (
            "Password must be at least 8 characters, not entirely numeric, "
            "and not too common."
        )
class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # User चा email update करू देणार

    class Meta:
        model = Profile
        fields = ['bio', 'avatar']  # Profile fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # current user मिळवण्यासाठी
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = user.email  # current email form मध्ये दाखवतो

    def save(self, commit=True):
        profile = super(EditProfileForm, self).save(commit=False)
        user = profile.user
        user.email = self.cleaned_data['email']  # email update करतो

        if commit:
            user.save()
            profile.save()
        return profile        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']   
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Write a caption...'})
        }       

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Add a comment...', 'class': 'comment-input'})
        }

class UserSearchForm(forms.Form):
    query = forms.CharField(max_length=150, label='Search Users', widget=forms.TextInput(attrs={'placeholder': 'Search by username'}))