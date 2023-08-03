import os
import io
import pandas
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from access_office.forms import CrossingPointForm, DocumentForm, AutomobileForm, DriverForm, \
    CustomStatusForm, PedestrianForm
from access_office.models import Document, CrossingPoint, Automobile, Driver, CustomStatus
from django.db.models import Q


class AccessOffice(LoginRequiredMixin, View):
    def get(self, request):
        context = dict()
        context['crossing_points'] = CrossingPoint.objects.all()
        context['documents'] = Document.objects.all()

        return render(request, 'access_office/access_office.html', context)

    def post(self, request):
        if 'export_to_excel' in request.POST:
            selected_record_ids = request.POST.getlist('selected_records')
            selected_records = Document.objects.filter(
                id__in=selected_record_ids)

            if (not selected_records) or (not selected_record_ids):
                error_no_record_selected = 'Вы не выбрали ни одной записи на выгрузку в Excel'
                context = dict()
                context['crossing_points'] = CrossingPoint.objects.all()
                context['documents'] = Document.objects.all()
                context['error_no_record_selected'] = error_no_record_selected
                return render(request, 'access_office/access_office.html', context)

            documents = list()

            for record in selected_records:
                document = list()
                document.append(dict(Document.status_choices)[record.status])
                document.append(record.number_of_document)
                document.append(record.title)
                document.append(record.date_start)
                document.append(record.date_end)
                document.append(record.comment_for_access_office)
                document.append(record.comment_for_security)
                document.append(','.join([str(cp) for cp in record.crossing_point_name.all()]))
                document.append(record.auto.driver.full_name)
                document.append(record.auto.driver.passport_details)
                document.append(record.auto.license_plate)
                document.append(record.auto.car_registration_number)
                document.append(record.auto.car_brand)
                documents.append(document)

            df = pandas.DataFrame.from_records(documents)
            df.columns = ['Статус документа', 'Номер документа', 'Название документа',
                          'Дата начала', 'Дата окончания', 'Комментарий бюро', 'Комментарий охраны',
                          'Пропускной пункт', 'ФИО Водителя',
                          'Паспортные данные водителя', 'Гос. рег. знак', 'Номер свидетельства о рег. ТС',
                          'Марка ТС']
            output = io.BytesIO()
            df.to_excel(output, index=False)

            response = HttpResponse(output.getvalue(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=records.xlsx'

            return response
        elif 'records_to_delete' in request.POST:
            context = dict()
            selected_record_ids = request.POST.getlist('selected_records')
            selected_records = Document.objects.filter(id__in=selected_record_ids).delete()

            return render(request, 'access_office/access_office.html', context)


class CreateCrossingPoint(LoginRequiredMixin, View):
    def get(self, request):
        form_crossing_point = CrossingPointForm()
        context = dict()
        context['form_crossing_point'] = form_crossing_point
        return render(request, 'access_office/create_crossing_point.html', context)

    def post(self, request):
        form_crossing_point = CrossingPointForm(request.POST)
        context = dict()
        context['form_crossing_point'] = form_crossing_point
        if form_crossing_point.is_valid():
            form_crossing_point.save()
            return redirect('access_office')
        else:
            context['error_crossing_point'] = 'Форма была заполнена некорректно'

        return render(request, 'access_office/create_crossing_point.html', context)


class CrossingPointView(LoginRequiredMixin, View):
    def get(self, request):
        context = dict()
        context['crossing_points'] = CrossingPoint.objects.all()
        return render(request, 'access_office/crossing_point.html', context)


class CrossingPointDelete(LoginRequiredMixin, View):
    def get(self, request, pk):
        crossing_point = CrossingPoint.objects.get(id=pk)
        crossing_point.delete()
        return redirect('crossing_point')


class CrossingPointUpdate(LoginRequiredMixin, View):
    def get(self, request, pk):
        record = CrossingPoint.objects.get(id=pk)
        form_crossing_point = CrossingPointForm(instance=record)

        context = dict()
        context['record'] = record
        context['form_crossing_point'] = form_crossing_point
        return render(request, 'access_office/crossing_point_update.html', context)

    def post(self, request, pk):
        record = CrossingPoint.objects.get(id=pk)
        form_crossing_point = CrossingPointForm(request.POST, instance=record)

        context = dict()
        context['record'] = record
        context['form_crossing_point'] = form_crossing_point

        if form_crossing_point.is_valid():
            form_crossing_point.save()
            return redirect('crossing_point')
        else:
            context['error_crossing_point'] = 'Форма была заполнена некорректно'

        return render(request, 'access_office/crossing_point_update.html')


class CreateDocument(LoginRequiredMixin, View):
    def get(self, request):
        form_document = DocumentForm()
        form_automobile = AutomobileForm()
        form_driver = DriverForm()
        form_pedestrian = PedestrianForm()
        context = dict()
        context['form_document'] = form_document
        context['form_automobile'] = form_automobile
        context['form_driver'] = form_driver
        context['form_pedestrian'] = form_pedestrian

        return render(request, 'access_office/create_document.html', context)

    def post(self, request):
        form_document = DocumentForm(request.POST, request.FILES)
        form_automobile = AutomobileForm(request.POST)
        form_driver = DriverForm(request.POST)
        form_pedestrian = PedestrianForm(request.POST)
        context = dict()
        context['form_document'] = form_document
        context['form_automobile'] = form_automobile
        context['form_driver'] = form_driver
        context['form_pedestrian'] = form_pedestrian
        if request.POST.get('form_to_check_document'):
            if form_document.is_valid():
                form_document.save()
                return redirect('access_office')
            else:
                context['error_document'] = 'Форма создания документа была заполнена некорректно'

        elif 'form_to_check_automobile' in request.POST:
            if form_automobile.is_valid():
                automobile = form_automobile.save()
                return JsonResponse(
                    {
                        'auto_id': automobile.id,
                        'license_plate': automobile.license_plate,
                    }
                )
            else:
                return JsonResponse(
                    {
                        'error_automobile': 'Форма создания автомобиля была заполнена некорректно',
                    }
                )

        elif 'form_to_check_driver' in request.POST:
            if form_driver.is_valid():
                driver = form_driver.save()
                return JsonResponse(
                    {
                        'driver_id': driver.id,
                        'driver': str(driver),
                    }
                )
            else:
                return JsonResponse(
                    {
                        'error_driver': 'Форма создания водителя была заполнена некорректно',
                    }
                )

        elif 'form_to_check_pedestrian' in request.POST:
            if form_pedestrian.is_valid():
                pedestrian = form_pedestrian.save()
                return JsonResponse(
                    {
                        'pedestrian_id': pedestrian.id,
                        'pedestrian': str(pedestrian),
                    }
                )
            else:
                return JsonResponse(
                    {
                        'error_driver': 'Форма создания водителя была заполнена некорректно',
                    }
                )

        return render(request, 'access_office/create_document.html', context)


class SearchDocument(View):
    def get(self, request):
        if request.GET.get('search'):
            search = request.GET['search']
            documents = Document.objects.all()
            if not request.user.is_authenticated:
                documents = documents.filter(status='W')
            print(documents[0].date_start)
            documents = documents.filter(
                Q(status__icontains=search)
                | Q(number_of_document__icontains=search)
                | Q(title__icontains=search)
                | Q(date_start__icontains=search)
                | Q(date_end__icontains=search)
                | Q(comment_for_access_office__icontains=search)
                | Q(comment_for_security__icontains=search)
                | Q(comment_import__icontains=search)
                | Q(comment_export__icontains=search)
                | Q(crossing_point_name__crossing_point_name__icontains=search)
                | Q(auto__license_plate__icontains=search)
                | Q(auto__car_brand__icontains=search)
                | Q(auto__driver__full_name__icontains=search)
                | Q(auto__driver__passport_details__icontains=search)
            )

            context = dict()
            context['documents'] = documents
            context['search'] = search
            return render(request, 'access_office/search_document.html', context)
        raise Http404()


class Security(View):
    def get(self, request):
        context = dict()
        context['documents'] = Document.objects.filter(status='W')
        context['crossing_points'] = CrossingPoint.objects.all()
        return render(request, 'access_office/security.html', context)


class SecurityPass(View):
    def get(self, request, pk):
        record = Document.objects.get(id=pk)

        context = dict()
        context['record'] = record

        return render(request, 'access_office/security_pass.html', context)

    def post(self, request, pk):
        record = Document.objects.get(id=pk)

        context = dict()
        context['record'] = record

        record.comment_for_security += request.POST.get('security_comment') + '\n\n'
        record.save()
        return redirect('security')


class UpdateDocument(LoginRequiredMixin, View):
    def get(self, request, pk):
        document_record = Document.objects.get(id=pk)
        automobile_record = Automobile.objects.get(id=document_record.auto.id)
        driver_record = Driver.objects.get(id=document_record.auto.driver.id)

        form_document = DocumentForm(instance=document_record)
        form_automobile = AutomobileForm(instance=automobile_record)
        form_driver = DriverForm(instance=driver_record)

        context = dict()
        context['form_document'] = form_document
        context['form_automobile'] = form_automobile
        context['form_driver'] = form_driver
        context['record'] = document_record
        context['file_name'] = os.path.basename(document_record.document_file.name)

        return render(request, 'access_office/update_document.html', context)

    def post(self, request, pk):
        document_record = Document.objects.get(id=pk)
        automobile_record = Automobile.objects.get(id=document_record.auto.id)
        driver_record = Driver.objects.get(id=document_record.auto.driver.id)

        form_document = DocumentForm(request.POST, request.FILES, instance=document_record)
        form_automobile = AutomobileForm(request.POST, instance=automobile_record)
        form_driver = DriverForm(request.POST, instance=driver_record)

        context = dict()
        context['form_document'] = form_document
        context['form_automobile'] = form_automobile
        context['form_driver'] = form_driver
        context['record'] = document_record

        if 'form_to_check_document' in request.POST:
            if form_document.is_valid():
                form_document.save()
                return redirect('access_office')
            else:
                error_document = 'Форма создания документа была заполнена некорректно'
                context['error_document'] = error_document

        elif 'form_to_check_automobile' in request.POST:
            if form_automobile.is_valid():
                automobile = form_automobile.save()

                return JsonResponse(
                    {
                        'auto_id': automobile.id,
                        'license_plate': automobile.license_plate,
                        'automobile_update': '',
                    }
                )
            else:
                error_automobile = 'Форма создания автомобиля была заполнена некорректно'
                return JsonResponse(
                    {
                        'error_automobile': error_automobile,
                    }
                )
        elif 'form_to_check_driver' in request.POST:
            if form_driver.is_valid():
                driver = form_driver.save()
                return JsonResponse(
                    {
                        'driver_id': driver.id,
                        'full_name': driver.full_name,
                        'driver_update': '',
                    }
                )
            else:
                error_driver = 'Форма создания водителя была заполнена некорректно'
                return JsonResponse(
                    {
                        'error_driver': error_driver,
                    }
                )

        return render(request, 'access_office/update_document.html', context)


class CreateCustomStatus(LoginRequiredMixin, View):
    def get(self, request):
        form_custom_status = CustomStatusForm()
        context = dict()
        context['form_custom_status'] = form_custom_status
        return render(request, 'access_office/create_custom_document_status.html', context)

    def post(self, request):
        form_custom_status = CustomStatusForm(request.POST)
        context = dict()
        context['form_custom_status'] = form_custom_status
        if form_custom_status.is_valid():
            form_custom_status.save()
            return redirect('access_office')
        else:
            context['error_custom_status'] = 'Форма была заполнена некорректно'

        return render(request, 'access_office/create_custom_document_status.html', context)


class CustomStatusView(LoginRequiredMixin, View):
    def get(self, request):
        context = dict()
        context['custom_statuses'] = CustomStatus.objects.all()
        print(context['custom_statuses'])
        return render(request, 'access_office/custom_status.html', context)


class CustomStatusUpdate(LoginRequiredMixin, View):
    def get(self, request, pk):
        record = CustomStatus.objects.get(id=pk)
        form_custom_status = CustomStatusForm(instance=record)

        context = dict()
        context['record'] = record
        context['form_custom_status'] = form_custom_status
        return render(request, 'access_office/custom_status_update.html', context)

    def post(self, request, pk):
        record = CustomStatus.objects.get(id=pk)
        form_custom_status = CustomStatusForm(request.POST, instance=record)

        context = dict()
        context['record'] = record
        context['form_custom_status'] = form_custom_status

        if form_custom_status.is_valid():
            form_custom_status.save()
            return redirect('custom_status_view')
        else:
            context['error_custom_status'] = 'Форма была заполнена некорректно'

        return render(request, 'access_office/custom_status_update.html')


class CustomStatusDelete(LoginRequiredMixin, View):
    def get(self, request, pk):
        custom_status = CustomStatus.objects.get(id=pk)
        custom_status.delete()
        return redirect('custom_status_view')
