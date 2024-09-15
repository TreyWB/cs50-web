from django import forms
from .models import Listings, Categories, Bids

class CreateListingForm(forms.ModelForm):
    title = forms.CharField(max_length=64)
    category = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        empty_label="Select a category",
        required=False
    )
    photo = forms.ImageField(required=False)
    initial_bid = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Listings  # Link this form to the Listing model
        fields = ['title', 'description', 'initial_bid', 'photo', 'category']  # Include the fields you want in the form
        exclude = ['user', 'watchlist_count']  # Exclude fields that are set programmatically or not needed

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)  # Remove 'user_id' from kwargs and store it in an instance variable
        super().__init__(*args, **kwargs)  # Call the parent class's __init__ with the remaining kwargs

    def save(self, commit=True):
        listing = super().save(commit=False)
        # Assign the user_id to the user field
        if self.user_id:
            listing.user_id = self.user_id
        if commit:
            listing.save()
        return listing


class BidForm(forms.ModelForm):
    bid = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Bids  # Link this form to the Bid model
        fields = ['bid']  # Include the fields you want in the form
        exclude = ['user', 'listing']  # Exclude fields that are set programmatically or not needed

    def __init__(self, *args, **kwargs):
        self.listing_id = kwargs.pop('listing_id', None)  # Remove 'listing_id' from kwargs and store it in an instance variable
        super().__init__(*args, **kwargs)  # Call the parent class's __init__ with the remaining kwargs

    def save(self, commit=True):
        bid = super().save(commit=False)
        # Assign the listing_id to the listing field
        if self.listing_id:
            bid.listing_id = self.listing_id
        if commit:
            bid.save()
        return bid