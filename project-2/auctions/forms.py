from django import forms
from .models import Listings, Categories, Bids, User


class CreateListingForm(forms.ModelForm):
    title = forms.CharField(max_length=64)

    category = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        empty_label="Select a category",
        required=False
    )

    photo_url = forms.URLField(required=False)
    initial_bid = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Listings
        fields = ['title', 'description', 'initial_bid', 'photo_url', 'category']
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        listing = super().save(commit=False)

        if self.user_id:
            listing.user_id = self.user_id
        if commit:
            listing.save()

        return listing


class BidForm(forms.ModelForm):
    bid = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Bids
        fields = ['bid']
        exclude = ['user', 'listing']

    def __init__(self, *args, **kwargs):
        self.listing_id = kwargs.pop('listing_id', None)
        self.user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        bid = cleaned_data.get('bid')

        if self.listing_id:
            listing = Listings.objects.get(id=int(self.listing_id))
            current_bid = listing.get_current_bid()

            if bid <= current_bid:
                raise forms.ValidationError("Bid must be greater than current bid.")

        return cleaned_data

    def save(self, commit=True):
        bid = super().save(commit=False)

        if self.listing_id:
            listing_instance = Listings.objects.get(id=int(self.listing_id))
            bid.listing = listing_instance
        if self.user_id:
            user_instance = User.objects.get(id=int(self.user_id))
            bid.user = user_instance

        if commit:
            bid.save()

        return bid