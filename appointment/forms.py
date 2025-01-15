from django import forms
from .models import Appointment
from datetime import datetime

class AppointmentForm(forms.ModelForm):
    TIME_CHOICES = [
        (f"{hour:02}:{minute:02}", f"{hour:02}:{minute:02}") 
        for hour in range(8, 18)  # From 08:00 to 17:30 with 30-minute intervals
        for minute in (0, 30)
    ]

    time = forms.ChoiceField(choices=TIME_CHOICES)
    
    # Set the minimum date to today
    today = datetime.today().date()
    day = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker'})
    )

    class Meta:
        model = Appointment
        fields = ['client_phone', 'day', 'time']

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        time = cleaned_data.get('time')

        # Check if day and time are provided
        if not day or not time:
            return cleaned_data

        # Check if day is in the past
        if day < self.today:
            raise forms.ValidationError("The date cannot be in the past.")

        # Check if time is in the past relative to today
        current_time = datetime.now().strftime('%H:%M')
        if day == self.today and time < current_time:
            raise forms.ValidationError("Laiko praeityje pasirinkti negalima")

        # Check if the selected day is a weekend
        if day.weekday() >= 5:  # 5 and 6 correspond to Saturday and Sunday
            raise forms.ValidationError("Vizitaii gali būti pasirenkami tik nuo Pirmadienio iki Penktadienio")

        # Check if an appointment already exists for the given day and time
        if Appointment.objects.filter(day=day, time=time).exists():
            raise forms.ValidationError("Šis laikas jau yra užimtas,pasirinkite sekančią dieną arba laiką")
        
        return cleaned_data
