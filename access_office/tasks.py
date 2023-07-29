from datetime import datetime
from access_office.models import Document
from access_system.celery import app
from django.db.models import Q


@app.task
def daily_check():
    documents_to_archive = Document.objects.filter(
        Q(date_end__lt=datetime.now().date()), ~Q(status__in=['A', 'N'])
    )

    for document_to_archive in documents_to_archive:
        if document_to_archive.comment_for_security == '':
            document_to_archive.status = 'N'
        else:
            document_to_archive.status = 'A'
        document_to_archive.save()
