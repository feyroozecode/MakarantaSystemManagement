from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.db.models import Sum

from apps.students.models import Student

from .forms import InvoiceItemFormset, InvoiceReceiptFormSet, Invoices
from .models import Invoice, InvoiceItem, Receipt


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    fields = "__all__"
    success_url = "/finance/list"

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        context['current_date'] = timezone.now()
        current_year = timezone.now().year
        #total_annulay_payement = Invoice.objects.filter(date__year=current_year).aggregate(total=Sum('total_amount_paid'))['total']
        #context['total_annulay_payement'] = total_annulay_payement if total_annulay_payement else 0
        
        if self.request.POST:
            context["items"] = InvoiceItemFormset(
                self.request.POST, prefix="invoiceitem_set"
            )
       
        else:
            context["items"] = InvoiceItemFormset(prefix="invoiceitem_set")
        return context


    def get_total_annualy_invoice(self, **kwargs):
        current_year = timezone.now().year
        total_annualy_invoice = Invoice.objects.filter(date__year=current_year).aggregate(total=Sum('total_amount_paid'))['total'] if Invoice.objects.filter(date__year=current_year).exists() else 0
        return total_annualy_invoice

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["items"]
        self.object = form.save()
        if self.object.id != None:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context["receipts"] = Receipt.objects.filter(invoice=self.object)
        context["items"] = InvoiceItem.objects.filter(invoice=self.object)
      
        context["current_date"] = timezone.now().strftime('%d/%m/%Y')
        # Generate a unique receipt number
        last_receipt = Receipt.objects.order_by('id').last()
        if last_receipt:
            next_number = last_receipt.id + 1
        else:
            next_number =  last_receipt.id + 1

        year_suffix = timezone.now().strftime('%y')
        receipt_number = f"REC/{year_suffix}-{next_number}"
        previous_balance = self.object.balance_from_previous_term if self.object.balance_from_previous_term else 0
        
        context["previous_balance"] = previous_balance  # Expose previous balance
        context["receipt_number"] = receipt_number

        return context


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    fields = ["student", "session", "term", "class_for", "balance_from_previous_term"]

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["receipts"] = InvoiceReceiptFormSet(
                self.request.POST, instance=self.object
            )
            context["items"] = InvoiceItemFormset(
                self.request.POST, instance=self.object
            )
        else:
            context["receipts"] = InvoiceReceiptFormSet(instance=self.object)
            context["items"] = InvoiceItemFormset(instance=self.object)
            
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["receipts"]
        itemsformset = context["items"]
        if form.is_valid() and formset.is_valid() and itemsformset.is_valid():
            form.save()
            formset.save()
            itemsformset.save()
        return super().form_valid(form)


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy("invoice-list")

class ReceiptCreateView(LoginRequiredMixin, CreateView):
    model = Receipt
    fields = ["amount_paid", "date_paid", "comment"]
    success_url = reverse_lazy("invoice-list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        obj.invoice = invoice
        obj.save()
        return redirect("invoice-list")

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateView, self).get_context_data(**kwargs)
        current_date = timezone.now()
        context["current_date"] = current_date
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        context["invoice"] = invoice
        return context


class ReceiptUpdateView(LoginRequiredMixin, UpdateView):
    model = Receipt
    fields = ["amount_paid", "date_paid", "comment"]
    success_url = reverse_lazy("invoice-list")


class ReceiptDeleteView(LoginRequiredMixin, DeleteView):
    model = Receipt
    success_url = reverse_lazy("invoice-list")


@login_required
def bulk_invoice(request):
    return render(request, "finance/bulk_invoice.html")


def get_absolute_url(self):
    return redirect(reverse('finance:create', kwargs={'user': self.pk}))