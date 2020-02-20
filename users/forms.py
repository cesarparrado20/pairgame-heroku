from django import forms

SI_NO = [
    ("no", "No"),
    ("si", "Sí"),
]


class ScrapingForm(forms.Form):
    opcion = forms.ChoiceField(
        choices=SI_NO,
        label="¿Scraping inicial?",
        help_text="Los scraping iniciales recorren 5 páginas, con el fin de obtener más "
                  "información."
    )

    def __init__(self, *args, **kwargs):
        super(ScrapingForm, self).__init__(*args, **kwargs)
        self.fields["opcion"].widget.attrs.update({
            "class": "form-control"
        })
