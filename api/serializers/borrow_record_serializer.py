from rest_framework import serializers
from ..models.borrow_record import BorrowRecord


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['id', 'user', 'book', 'borrow_date', 'return_date']
