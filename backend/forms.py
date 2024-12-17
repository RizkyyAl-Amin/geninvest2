from django import forms
from .models import Article
from .models import Produk
from .models import MonthlyReport

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['judul', 'kategori', 'konten', 'cover']
        widgets = {
           'judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan judul artikel'}),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'konten': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'cover': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['kode_saham',  'nama_perusahaan', 'jenis_saham', 'saham']

class MonthlyReportForm(forms.ModelForm):
    class Meta:
        model = MonthlyReport
        fields = ['imba_hasil', 'report_file']

    def clean_report_file(self):
        file = self.cleaned_data.get('report_file', None)
        if file:
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("File harus berupa PDF.")
        return file