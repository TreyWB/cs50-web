from django import forms
from .models import Listings, Categories, Bids, User

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

# class EditListingForm(forms.ModelForm):
#     class Meta:
#         model = Listings  # Link this form to the Listings model
#         fields = ['title', 'description', 'initial_bid', 'photo', 'category']  # Include the fields you want in the form
#         exclude = ['user', 'watchlist_count']  # Exclude fields that are set programmatically or not needed
        
#         # Customize widgets if needed
#         widgets = {
#             'title': forms.TextInput(attrs={'maxlength': 64}),
#             'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
#             'initial_bid': forms.NumberInput(attrs={'step': 0.01}),
#             'photo': forms.ClearableFileInput(),
#             'category': forms.Select(attrs={'class': 'form-control'})
#         }

#     # def __init__(self, *args, **kwargs):
#     #     self.user_id = kwargs.pop('user_id', None)  # Remove 'user_id' from kwargs and store it in an instance variable
#     #     super().__init__(*args, **kwargs)  # Call the parent class's __init__ with the remaining kwargs

#     def save(self, commit=True):
#         listing = super().save(commit=False)
#         if self.user_id:
#             listing.user_id = self.user_id
#         if commit:
#             listing.save()
#         return listing

class BidForm(forms.ModelForm):
    bid = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Bids  # Link this form to the Bids model
        fields = ['bid']  # Include only the fields you want in the form
        exclude = ['user', 'listing']  # Exclude fields that are set programmatically

    def __init__(self, *args, **kwargs):
        self.listing_id = kwargs.pop('listing_id', None)  # Remove 'listing_id' from kwargs and store it in an instance variable
        self.user_id = kwargs.pop('user_id', None)  # Remove 'user_id' from kwargs and store it in an instance variable
        super().__init__(*args, **kwargs)  # Call the parent class's __init__ with the remaining kwargs

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

        # Debugging: Print the values to ensure they are correct
        print(f"Saving bid for listing_id: {self.listing_id}, user_id: {self.user_id}")

        # Correctly assign the listing and user instances to the foreign key fields
        if self.listing_id:
            listing_instance = Listings.objects.get(id=int(self.listing_id))  # Ensure the ID is an integer
            bid.listing = listing_instance  # Assign the Listing instance

        if self.user_id:
            user_instance = User.objects.get(id=int(self.user_id))  # Ensure the ID is an integer
            bid.user = user_instance  # Assign the User instance

        if commit:
            bid.save()
        return bid