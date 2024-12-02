from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.borrow_record import BorrowRecord
from ..serializers.borrow_record_serializer import BorrowRecordSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.conf import settings


class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]
    storage_service = settings.STORAGE_SERVICE

    @action(detail=False, methods=['post'])
    def borrow(self, request):
        book_id = request.data.get('book')
        user = request.user

        if self.storage_service.retrieve(BorrowRecord, user=user, book_id=book_id, return_date__isnull=True).exists():
            return Response({"error": "You have already borrowed this book"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'user': user.id, 'book': book_id})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance = self.storage_service.save(instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def return_book(self, request):
        book_id = request.data.get('book')
        user = request.user

        try:
            borrow_record = self.storage_service.retrieve(BorrowRecord, user=user, book_id=book_id,
                                                          return_date__isnull=True).get()
        except BorrowRecord.DoesNotExist:
            return Response({"error": "You haven't borrowed this book"}, status=status.HTTP_400_BAD_REQUEST)

        borrow_record.return_date = timezone.now()
        borrow_record = self.storage_service.update(borrow_record, return_date=borrow_record.return_date)

        serializer = self.get_serializer(borrow_record)
        return Response(serializer.data)
