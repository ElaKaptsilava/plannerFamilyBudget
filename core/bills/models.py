from accounts.models import UserAbstractModel
from django.db import models


class Bill(UserAbstractModel):
    creditor = models.CharField(max_length=100, help_text="The name of the creditor")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="The total amount of the bill"
    )
    start_date = models.DateField(auto_now_add=True)
    deadline = models.DateField(help_text="The due date of the bill")

    def __str__(self) -> str:
        return f"Bill from {self.creditor} - Amount: {self.amount}"

    def __repr__(self) -> str:
        return (
            f"<Bill(id={self.id}, user={self.user}, creditor='{self.creditor}', "
            f"amount={self.amount}, deadline={self.deadline})>"
        )

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"


class Transaction(UserAbstractModel):
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name="transactions",
        help_text="The bill associated with this transaction",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="The amount paid in this transaction"
    )
    date = models.DateField(
        auto_now_add=True, help_text="The date the transaction was made"
    )

    def __str__(self) -> str:
        return f"Transaction of {self.amount} on {self.date}"

    def __repr__(self) -> str:
        return (
            f"<Transaction(id={self.id}, bill_id={self.bill.id}, amount={self.amount}, "
            f"date={self.date})>"
        )

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["date"]
