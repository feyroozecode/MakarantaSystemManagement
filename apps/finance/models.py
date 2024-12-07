from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, date

from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass
from apps.students.models import Student


class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    class_for = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    balance_from_previous_term = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("closed", "Closed")],
        default="active",
    )

    class Meta:
        ordering = ["student", "term"]

    def __str__(self):
        return f"{self.student} "

    def created_at(self):
        """Returns the creation datetime of the invoice"""
        if self.receipt_set.exists():
            # Get the first receipt's datetime
            first_receipt = self.receipt_set.order_by('date_paid').first()
            # Combine date with default time if no time component
            return timezone.make_aware(datetime.combine(first_receipt.date_paid, datetime.min.time())) if isinstance(first_receipt.date_paid, date) else first_receipt.date_paid
        elif hasattr(self.session, 'current') and self.session.current:
            return timezone.now()
        elif hasattr(self.session, 'start_date') and self.session.start_date:
            # Convert date to datetime if necessary
            return timezone.make_aware(datetime.combine(self.session.start_date, datetime.min.time())) if isinstance(self.session.start_date, date) else self.session.start_date
        elif hasattr(self.term, 'current') and self.term.current:
            return timezone.now()
        elif hasattr(self.term, 'start_date') and self.term.start_date:
            # Convert date to datetime if necessary
            return timezone.make_aware(datetime.combine(self.term.start_date, datetime.min.time())) if isinstance(self.term.start_date, date) else self.term.start_date
        return timezone.now()

    def balance(self):
        payable = self.total_amount_payable()
        paid = self.total_amount_paid()

        return payable - paid

    def amount_payable(self):
        items = InvoiceItem.objects.filter(invoice=self)
        total = 0
        for item in items:
            total += item.amount
        return total

    def total_amount_payable(self):
        return self.balance_from_previous_term + self.amount_payable()

    def total_amount_paid(self):
        receipts = Receipt.objects.filter(invoice=self)
        amount = 0
        for receipt in receipts:
            amount += receipt.amount_paid
        return amount

    def get_absolute_url(self):
        return reverse("invoice-detail", kwargs={"pk": self.pk})
    
    def last_payment(self):
        return Receipt.objects.filter(invoice=self).order_by('-date_paid').first()

    def total_annual(self):
        # Get all invoices for this student in the current session
        student_invoices = Invoice.objects.filter(
            student=self.student,
            session=self.session
        )
        total = 0
        for invoice in student_invoices:
            total += invoice.total_amount_payable()
        return total

    def total_annual_paid(self):
        # Get all invoices for this student in the current session
        student_invoices = Invoice.objects.filter(
            student=self.student,
            session=self.session
        )
        total = 0
        for invoice in student_invoices:
            total += invoice.total_amount_paid()
        return total

    def total_annual_balance(self):
        return self.total_annual() - self.total_annual_paid()


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.IntegerField()


class Receipt(models.Model):
    current_date = timezone.now()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    date_paid = models.DateField(default=timezone.now)
    comment = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Receipt on {self.date_paid}"
